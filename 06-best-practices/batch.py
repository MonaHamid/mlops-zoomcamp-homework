#!/usr/bin/env python
# coding: utf-8

import os
import sys
import pickle
import pandas as pd
import s3fs # Make sure to install this: pip install s3fs

def get_path(pattern_env_var, default_pattern, year, month):
    """
    Retrieves the file path from an environment variable pattern,
    formatting it with the given year and month.
    """
    pattern = os.getenv(pattern_env_var, default_pattern)
    return pattern.format(year=year, month=month)

def prepare_data(df, categorical):
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df
    
def read_data(filename, categorical, s3_endpoint_url=None):
    """
    Reads a parquet file from the given filename and prepares the data.
    Handles S3 paths if s3_endpoint_url is provided.
    """
    options = {}
    if filename.startswith('s3://') and s3_endpoint_url:
        options['client_kwargs'] = {
            'endpoint_url': s3_endpoint_url
        }
    
    df = pd.read_parquet(filename, storage_options=options)
    return prepare_data(df, categorical)

def save_data(df, output_path, s3_endpoint_url=None):
    """
    Saves a DataFrame to a parquet file at the specified output_path.
    Handles S3 paths if s3_endpoint_url is provided.
    If the path is a local file path (starts with 'file://'), it ensures
    the directory exists before saving.
    """
    options = {}
    if output_path.startswith('s3://') and s3_endpoint_url:
        options['client_kwargs'] = {
            'endpoint_url': s3_endpoint_url
        }
    elif output_path.startswith("file://"):
        local_path = output_path.replace("file://", "")
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        output_path = local_path # Use local path for pandas to write directly

    df.to_parquet(
        output_path,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options
    )

def main(year, month):
    # Get input and output file paths using environment variables
    input_file = get_path(
        "INPUT_FILE_PATTERN", 
        f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet',
        year, month
     )
    output_file = get_path(
        "OUTPUT_FILE_PATTERN", 
        f'taxi_type=yellow_year={year:04d}_month={month:02d}.parquet', # Original hardcoded default
        year, month
    )
    s3_endpoint_url = os.getenv('S3_ENDPOINT_URL', None)

    print('Input file:', input_file)
    print('Output file:', output_file)
    print('S3 Endpoint URL:', s3_endpoint_url)
    
    # Load the pre-trained model and DictVectorizer
    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)
    
    categorical = ['PULocationID', 'DOLocationID']
        
    # Read and prepare the input data
    df = read_data(input_file, categorical, s3_endpoint_url)

    # Generate ride_id
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    
    # Transform categorical features and make predictions
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    
    print('Mean predicted duration:', y_pred.mean())
    print('Sum predicted duration:', y_pred.sum()) # Added this print for easier debugging
    
    # Create a DataFrame for results
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred
    
    # Save the results using the new save_data function
    save_data(df_result, output_file, s3_endpoint_url)


if __name__ == '__main__':
    # Default year and month for standalone execution
    year = 2023 
    month = 1 
    main(year, month)
