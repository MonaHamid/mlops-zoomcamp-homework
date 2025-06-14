from prefect import flow, task
from batch import run

@task
def load_model():
    import pickle
    with open("model.bin", "rb") as f_in:
        dv, model = pickle.load(f_in)
    return dv, model

@task
def read_data(year, month):
    import pandas as pd
    input_file = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-04.parquet"
    df = pd.read_parquet(input_file)
    return df

@task
def make_predictions(dv, model, df):
    features = ["PULocationID", "DOLocationID", "trip_distance"]
    X_dict = df[features].fillna(0).to_dict(orient="records")
    X = dv.transform(X_dict)
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
    dv, model = load_model()
    df = read_data(year, month)
    preds = make_predictions(dv, model, df)
    output_path = save_predictions(preds, year, month)
    print(f"Saved to {output_path}")