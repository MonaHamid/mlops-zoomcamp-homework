#!/usr/bin/env python
# coding: utf-8

# # MLOps Zoomcamp – Week 3 Homework (Mage + MLflow)
# 
# This notebook contains:
# - All 6 homework questions (as markdown)
# - Code to answer each question
# - MLflow tracking
# 

# 
# ## Question 1. Select the Tool  
# **What's the name of the orchestrator you chose?**  
# → Answer: Mage  
# ## Question 2. Version  
# **What's the version of the orchestrator?**  
# → Answer: Mage version `0.9.76

# In[7]:


#Q3 Load Data

import pandas as pd

url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet"
df = pd.read_parquet(url)
print("Q3 - Raw data shape:", df.shape)


# ## Question 4. Data preparation  
# Clean the data using the following logic:
# - Calculate `duration`
# - Filter out rides shorter than 1 or longer than 60 minutes
# - Convert categorical columns to string
# 
# What's the size of the result?  
# → Options: 2,903,766 | 3,103,766 | 3,316,216 | 3,503,766
# 

# In[8]:


#Q4 Clean Data

df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
df['duration'] = df['duration'].dt.total_seconds() / 60

df = df[(df.duration >= 1) & (df.duration <= 60)]
df[['PULocationID', 'DOLocationID']] = df[['PULocationID', 'DOLocationID']].astype(str)
print("Q4 - Cleaned data shape:", df.shape)


# ## Question 5. Train a Model  
# Train a linear regression using pickup/dropoff IDs as features.  
# Use `DictVectorizer`. Don't combine features.
# 
# What is the intercept?  
# → Options: 21.77 | 24.77 | 27.77 | 31.77
# 

# In[9]:


from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression

train_dicts = df[['PULocationID', 'DOLocationID']].to_dict(orient='records')

dv = DictVectorizer()
X_train = dv.fit_transform(train_dicts)
y_train = df['duration'].values

model = LinearRegression()
model.fit(X_train, y_train)

print("Q5 - Intercept:", round(model.intercept_, 2))


# ## Question 6. Register the Model  
# Log the model using MLflow. Check the size of the `MLmodel` file.
# 
# What’s the size of the model?  
# → Options: 14,534 | 9,534 | 4,534 | 1,534
# 

# In[10]:


import mlflow
import mlflow.sklearn

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("nyc-taxi")

with mlflow.start_run():
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_param("intercept", model.intercept_)
    mlflow.sklearn.log_model(model, "model")

