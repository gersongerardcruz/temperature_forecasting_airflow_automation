# End-to-End Weather Forecasting with Apache Airflow Automation

## Project Information

[Apache Airflow](https://airflow.apache.org/) is an open-source platform designed to programmatically author, schedule, and monitor workflows. It allows users to create complex workflows, called DAGs (Directed Acyclic Graphs), which are made up of tasks that can be chained together to form a complete data pipeline. Each task is a unit of work that performs a specific operation, such as extracting data from a source, transforming it, and loading it into a target system. 

Airflow's primary benefit is its ability to manage and automate complex workflows. It provides a user-friendly interface to create and monitor workflows, as well as powerful tools for managing dependencies and executing tasks in parallel. With Airflow, data engineers can easily create and manage pipelines that incorporate data from multiple sources, perform complex transformations, and load the results into target systems. By automating these workflows, Airflow enables data engineers to focus on higher-level tasks, such as designing data models and creating data visualizations, rather than spending time on manual, repetitive tasks.

In this project, I learn about Apache Airflow and use it to automate a weather forecasting project from API data collection up to model deployment and prediction. The project pipeline is as in the diagram below:

![pipeline](images/pipeline.jpg)

The pipeline operates as follows:
1. Data is collected using the [Open-Meteo API](https://github.com/m0rp43us/openmeteopy) which offers free weather forecast APIs. This allows the user to get free two-day historical data in any location. For the purpose of this project, two days will be enough to simulate a real-time environment. 
2. Python scripts are used to perform the data collection, data preprocessing, and model training. 
3. On an AWS EC2 Ubuntu server, apache airflow is deployed and DAGs are created to automate the data collection, preprocessing, model training, and model prediction. 
4. The resulting files from automation are then stored in AWS S3. 

## Business Value

## Technical Value

## Project Structure

## Key Project Files

## Project Instructions

### Setting up

### Preprocessing

### Training
 
### Deployment

### Demo

## Conclusions

## Recommendations

## References
