import pandas as pd
import h2o
import mlflow
import mlflow.h2o
import io
import sys
import os
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
from fastapi import FastAPI, File 
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import *

# Set up an H2O cluster
h2o.init()
    
# Spin up Mlflow client
client = MlflowClient()

# Get the best model in the experiment used for training by first
# getting all experiments and searching for run with highest auc metric
experiments = mlflow.search_experiments(view_type=ViewType.ACTIVE_ONLY)
experiment_ids = [exp.experiment_id for exp in experiments]
runs_df = mlflow.search_runs(
    experiment_ids=experiment_ids,  # List of experiment IDs to search
    run_view_type=ViewType.ACTIVE_ONLY, # View all runs
    order_by=["metrics.best_model_logloss DESC"],  # Metrics to sort by and sort order
    max_results=1  # Maximum number of runs to return
)

# Extract the run_id and experiment_id of the top run
run_id = runs_df.iloc[0]["run_id"]
experiment_id = runs_df.iloc[0]["experiment_id"]

# Load best model based on experiment and run ids
best_model = mlflow.h2o.load_model(f"mlruns/{experiment_id}/{run_id}/artifacts/h2o_automl_model/")
best_model_uri = mlflow.get_artifact_uri(f"mlruns/{experiment_id}/{run_id}/artifacts/h2o_automl_model/")

# Create a FastAPI app
app = FastAPI()

# Define the endpoint for prediction
@app.post("/predict")
async def predict(file: bytes = File(...)):

    # Read the uploaded CSV file in bytes format and convert to pandas dataframe
    data = io.BytesIO(file)
    test_df = pd.read_csv(data)
    test_df = remove_id_column(test_df)
    test_df = h2o.H2OFrame(test_df)

    print(test_df)

    # Generate predictions using the best model
    preds = best_model.predict(test_df)
    preds = preds.as_data_frame()['predict']

    # Convert predictions to json file
    json_compatible_item_data = jsonable_encoder(preds)
    return JSONResponse(content=json_compatible_item_data)

