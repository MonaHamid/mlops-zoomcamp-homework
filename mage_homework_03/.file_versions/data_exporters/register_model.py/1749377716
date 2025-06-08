import mlflow
import pickle

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data(train_model, **kwargs):
    # Unpack model and vectorizer
    model, dv = train_model

    # ✅ Connect to MLflow running in the Docker container
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("homework_3_tracking")

    with mlflow.start_run():
        mlflow.sklearn.log_model(model, artifact_path="lin_reg_model")

        filename = "dict_vectorizer.pkl"
        with open(filename, "wb") as f_out:
            pickle.dump(dv, f_out)
        mlflow.log_artifact(filename, artifact_path="preprocessor")

    return model
