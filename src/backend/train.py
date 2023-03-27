import sys
import os

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import *
import h2o
import mlflow
import joblib
from mlflow.tracking import MlflowClient
from h2o.automl import H2OAutoML, get_leaderboard

df = pd.read_csv("data/processed/train.csv", index_col=0)

def train_automl_model(train_data: pd.DataFrame, target_column: str, max_models: int = 15, 
                       run_name: str = "weather-forecasting"):
    """
    Trains an H2O AutoML model on the given training data using the given target column.

    Args:
        train_data (pd.DataFrame): Training data with columns for features and target.
        target_column (str): The name of the target column.
        max_models (int): Maximum number of models to train in AutoML. Default is 10.
        run_name (str): Name of the MLflow experiment run. Default is "weather-forecasting".
    """

    # Initiate H2O cluster
    h2o.init()

    client = MlflowClient()

    # Remove ID column if it exists
    train_data = remove_id_column(train_data)

    # Convert training data to H2O frame
    train_data = h2o.H2OFrame(train_data)

    # Set the names of the feature columns
    feature_cols = [col for col in train_data.columns if col != target_column]

    # Ensure that H2O automl recognizes this as a regression task
    train_data[target_column] = train_data[target_column].asnumeric()

    # Start an MLflow experiment for tracking
    mlflow.set_experiment(run_name)

    # Start an MLflow run for tracking the AutoML experiment
    with mlflow.start_run():
        
        # Get the ID of the current MLflow run
        run_id = mlflow.active_run().info.run_id

        # Split the training data into training and validation sets
        train, valid = train_data.split_frame(ratios=[0.8], seed=0)
        
        # Train an H2O AutoML model
        automl = H2OAutoML(max_models=max_models, seed=0, sort_metric='rmse', verbosity='info', max_runtime_secs=3600)
        automl.train(x=feature_cols, y=target_column, training_frame=train, validation_frame=valid)
        
        # Log the AutoML leaderboard to MLflow and save it as a CSV file
        leaderboard = automl.leaderboard.as_data_frame()
        leaderboard.to_csv('references/leaderboard.csv', index=False)
        mlflow.log_param('max_models', max_models)
        mlflow.log_metric('rmse', leaderboard['rmse'][0])
        mlflow.log_artifact('references/leaderboard.csv')

        # Get the best model from the leaderboard
        best_model_id = leaderboard.loc[0, "model_id"]
        best_model = h2o.get_model(best_model_id)

        # Save the model using joblib
        joblib.dump(best_model, "ec2_airflow/model/model.pkl")

        # Save the H2O model to disk locally to prepare for ec2 deployment in case of h2o usage
        model_path = h2o.download_model(best_model, path='ec2_airflow/model/')

        # Log the H2O model artifact to MLflow
        client.log_artifact(run_id, model_path)
        mlflow.h2o.log_model(best_model, "h2o_automl_model")

        leaderboard_uri = mlflow.get_artifact_uri("references/leaderboard.csv")
        best_model_uri = mlflow.get_artifact_uri("h2o_automl_model")

        print(f"The leaderboard is located at: {leaderboard_uri}")
        print(f"The best model is located at: {best_model_uri}")

        # Evaluate the performance of the best model on the validation set
        best_model_performance = best_model.model_performance(valid)

        print(f"The validation rmse is: {best_model_performance.rmse()}")

        # Log the performance of the best model on the validation set
        mlflow.log_metric("best_model_logloss", best_model_performance.rmse())

        h2o.cluster().shutdown()

train_automl_model(df, target_column="apparent_temperature")