import os
import pickle
import click
import mlflow

from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error


# Constants
HPO_EXPERIMENT_NAME = "random-forest-hyperopt"
EXPERIMENT_NAME = "random-forest-best-models"
MODEL_NAME = "nyc-taxi-rf-model"
RF_PARAMS = ['max_depth', 'n_estimators', 'min_samples_split', 'min_samples_leaf', 'random_state']

# MLflow config
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment(EXPERIMENT_NAME)
mlflow.sklearn.autolog()


def load_pickle(filename):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


def train_and_log_model(data_path, params):
    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))
    X_test, y_test = load_pickle(os.path.join(data_path, "test.pkl"))

    with mlflow.start_run():
        new_params = {}

        for param in RF_PARAMS:
            value = params.get(param)
            try:
                new_params[param] = int(float(value))
            except (ValueError, TypeError):
                print(f"⚠️ Could not cast {param}='{value}' to int. Skipping.")
                return  # Skip this run if parameters are malformed

        rf = RandomForestRegressor(**new_params)
        rf.fit(X_train, y_train)

        val_rmse = root_mean_squared_error(y_val, rf.predict(X_val))
        test_rmse = root_mean_squared_error(y_test, rf.predict(X_test))

        mlflow.log_metric("val_rmse", val_rmse)
        mlflow.log_metric("test_rmse", test_rmse)

        mlflow.sklearn.log_model(rf, artifact_path="model")


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
@click.option(
    "--top_n",
    default=5,
    type=int,
    help="Number of top models that need to be evaluated to decide which one to promote"
)
def run_register_model(data_path: str, top_n: int):
    client = MlflowClient()

    # Get top N runs from HPO experiment
    hpo_experiment = client.get_experiment_by_name(HPO_EXPERIMENT_NAME)
    if hpo_experiment is None:
        raise RuntimeError(f"Experiment '{HPO_EXPERIMENT_NAME}' not found!")

    runs = client.search_runs(
        experiment_ids=hpo_experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=top_n,
        order_by=["metrics.rmse ASC"]
    )

    for run in runs:
        train_and_log_model(data_path=data_path, params=run.data.params)

    # Get best run from new experiment
    best_exp = client.get_experiment_by_name(EXPERIMENT_NAME)
    if best_exp is None:
        raise RuntimeError(f"Experiment '{EXPERIMENT_NAME}' not found!")

    best_run = client.search_runs(
        experiment_ids=best_exp.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=1,
        order_by=["metrics.test_rmse ASC"]
    )[0]

    best_model_uri = f"runs:/{best_run.info.run_id}/model"
    mlflow.register_model(model_uri=best_model_uri, name=MODEL_NAME)

    print("\n Best model registered successfully!")
    print(f" Model name: {MODEL_NAME}")
    print(f" URI: {best_model_uri}")
    print(f" View run: http://127.0.0.1:5000/#/experiments/{best_exp.experiment_id}/runs/{best_run.info.run_id}")


if __name__ == '__main__':
    run_register_model()
