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

Business using Airflow to automate their data pipelines and processes can derive value by having: 

* Financial savings: By automating the end-to-end data pipeline with Airflow, you can minimize manual effort and reduce labor costs associated with repetitive tasks, resulting in cost savings.
* Time savings: Airflow allows for easy scheduling and automation of data collection, preprocessing, model training, and prediction tasks, saving valuable time for the business and enabling faster decision-making.
* Improved efficiency: With Airflow, you can create complex workflows with dependencies and monitoring, which helps optimize the data pipeline and improve overall operational efficiency.
* Scalability: Airflow is designed to scale horizontally, allowing your business to handle large datasets and increasing the capacity for data processing as your business grows.

## Technical Value

Technical teams can generate value by using Airflow in their workflows by having:

* Workflow automation: Airflow enables the automation of complex data workflows, allowing data scientists and engineers to define, schedule, and orchestrate data pipelines as code. This helps reduce manual effort and human error, improving the overall efficiency and reliability of the data pipeline.
* Modularity and extensibility: Airflow provides a modular and extensible architecture that allows data scientists and engineers to easily integrate with various data sources, data processing libraries, and machine learning frameworks. This makes it highly adaptable to different data engineering and data science use cases, and promotes code reusability and maintainability.
* Flexibility and customization: Airflow provides a flexible and customizable platform that allows data scientists and engineers to tailor the data pipeline to their specific needs. It allows for custom operators, hooks, and sensors to be created, and provides support for plugins, making it highly adaptable to unique data engineering and data science requirements.
* Ease of use and developer-friendly structure: Airflow offers a user-friendly web-based UI for managing workflows, making it easy for data scientists and engineers to monitor and manage their data pipelines. It also provides a Pythonic API and CLI for defining, deploying, and managing workflows as code, making it developer-friendly and accessible to data scientists and engineers with Python programming skills.

## Project Structure

    ├── README.md          <- The top-level documentation for this project.
    ├── data
    │   ├── processed      <- The final data sets for customer segmentation.
    │   ├── interim        <- Folder for holding data with intermediate transformations
    │   └── raw            <- The original, immutable datasets.
    ├── ec2_airflow        <- 
    │   ├── dag            <- Folder containing scripts for deploying airflow in ec2
    ├── images             <- The media used in the README documentation
    ├── requirements.txt   <- The requirements file for reproducing the project
    ├── src                <- Folder containing all source code in the project
    │   ├── backend        <- Folder for all files for setting up the backend 
    │   ├── frontend       <- Folder for all files for setting up the frontend

## Key Project Files

- `data/`: Folder containing sample data gathered from Open-Meteo
    - `raw/`: Folder containing raw gathered data
    - `processed/`: Folder containing for-training data after being preprocessed
- `ec2_airflow`: Folder containing scripts for using airflow in AWS EC2 instance
    - `dag/`
        - `dag.py`: Python file containing airflow script for constructing a four-step DAG from data collection to model prediction
- `src`: Folder containing Python scripts for collecting data, preprocessing data, and training an ML model
    - `get_data.py`: Python file for using Open-Meteo to collect two-day historical weather data
    - `utils.py`: Python file containing all helper functions for data gathering, preprocessing, and model training
    - `preprocess.py`: Python file for performing preprocessing steps such as creating lag windows
    - `train.py`: Python file for training an XGBoost model for forecasting

## Project Instructions

### Setting up

### Preprocessing

### Training
 
### Deployment

### Demo

## Conclusions

## Recommendations

## References
