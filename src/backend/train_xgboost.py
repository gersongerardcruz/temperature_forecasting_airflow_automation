import pandas as pd
import xgboost as xgb
import os
import sys
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from joblib import dump

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import *

df = pd.read_csv("data/processed/train.csv", index_col=0)

def train_xgboost(df, model_path):
    # Split the data into training and testing sets
    X = df.drop("apparent_temperature", axis=1)
    y = df["apparent_temperature"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the XGBoost model
    model = xgb.XGBRegressor(objective="reg:squarederror", random_state=42)
    model.fit(X_train, y_train)
    
    # Save the model
    dump(model, model_path, protocol=2)

    # Make predictions on the test set
    y_pred = model.predict(X_test)
    
    # Print out the relevant metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print("Mean squared error:", mse)
    print("R-squared:", r2)

train_xgboost(df, "ec2_airflow/model/model.pkl")