from prefect import flow, task
from batch import run

@task
def load_model():
    import pickle
    with open("model.bin", "rb") as f_in:
        return pickle.load(f_in)

@task
def read_data(year, month):
    import pandas as pd
    input_file = f"https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_{year}-{month:02d}.parquet"
    df = pd.read_parquet(input_file)
    return df

@task
def make_predictions(model, df):
    features = ["PULocationID", "DOLocationID", "trip_distance"]
    X = df[features].fillna(0)
    return model.predict(X)

@task
def save_predictions(preds, year, month):
    import pickle
    import os
    output_file = f"output_{year}_{month}.bin"
    with open(output_file, "wb") as f_out:
        pickle.dump(preds, f_out)
    return output_file

@flow
def taxi_duration_pipeline(year: int = 2023, month: int = 4):
    model = load_model()
    df = read_data(year, month)
    preds = make_predictions(model, df)
    output_path = save_predictions(preds, year, month)
    print(f"Saved to {output_path}")