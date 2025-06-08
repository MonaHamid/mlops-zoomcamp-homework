 MLOps Zoomcamp Homework 03 – NYC Taxi Duration Model with Mage

This project trains a linear regression model to predict taxi trip durations using the NYC Yellow Taxi dataset for March 2023. All steps are performed inside Mage, and the final model is logged to MLflow.

 Question 1. Run Mage

Goal: Launch Mage using Docker Compose.

 Mage Version: v0.9.76

mage start <project_name>

<img width="941" alt="image" src="https://github.com/user-attachments/assets/bbf9dddf-10ba-4570-84af-ebff7ecc5f64" />


 Question 2. Creating a project

Task: Create a new Mage project named homework_03.

 metadata.yaml line count: 55 lines

wc -l mage_homework_03/metadata.yaml

![metadata yml](https://github.com/user-attachments/assets/3e1f483f-04bd-419e-a6ec-6db69045e68e)



 Question 3. Creating a pipeline

Task: Create an ingestion block that reads the March 2023 Yellow Taxi Parquet file.

 Loaded rows: 3,403,766
<img width="539" alt="image" src="https://github.com/user-attachments/assets/b465f109-f4f3-431b-bd4b-3afc18bbfd9a" />




 Question 4. Data Preparation

Task: Clean and filter the dataset for modeling.

 Filtered rows: 3,316,216

<img width="551" alt="image" src="https://github.com/user-attachments/assets/1d857b1e-7561-49f8-a141-50397a12e03e" />





 Question 5. Train a Model

Task: Train a linear regression model using DictVectorizer.

 Model Intercept: 23.848739685890877
<img width="545" alt="image" src="https://github.com/user-attachments/assets/42106a85-95cc-4939-9fd7-7460e6fffeb6" />




 Question 6. Register the model with MLflow

Task: Log model and vectorizer to MLflow.

 MLmodel Size: 4,542 bytes
<img width="927" alt="image" src="https://github.com/user-attachments/assets/aa375ceb-4ac1-4142-9ec6-08bf92c55acb" />








