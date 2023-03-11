import streamlit as st
import pandas as pd
import h2o
from utils import *
import json 

h2o.init()

# Set app title
st.title('End-to-End Weather Temperature Forecasting')

# Define a placeholder for the uploaded file data
file_data = None

# Define a placeholder for the predictions
predictions = None

# Use st.file_uploader to get a file from the user
st.caption("Choose file for classification here")
file = st.file_uploader('Upload files', type=['csv', 'xlsx'], label_visibility='visible')

# If a file was uploaded
if file is not None:

    st.caption("Check if your uploaded data is correct: ")

    # Use pandas to read the file into a dataframe
    file_data = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)

    file_data = remove_id_column(file_data)

    # Write the dataframe head to the app for the user to check
    st.write(file_data.head())

# If the user has uploaded a file and wants to make predictions
if file_data is not None and st.button('Predict'):

    st.caption("Prediction in progress...")

    # Use st.progress to display a progress bar while predictions are being made
    progress_bar = st.progress(0)

    test_df = h2o.H2OFrame(file_data)
    model = h2o.load_model("model/model")

    # Make a prediction using the trained model and display results
    preds = model.predict(test_df)
    preds = preds.as_data_frame()["predict"]
    preds = preds.to_json()

    # Update progress bar to 100%
    progress_bar.progress(100)

    # If predictions have been made, display a download button for the predictions
    if preds is not None:        
        
        st.success("Prediction successful! Please download your results")

        # Use st.download_button to allow the user to download the predictions as a CSV file
        st.download_button(
            label='Download predictions',
            data=json.dumps(preds),
            file_name='predictions.json',
            mime='application/json'
        )
    

