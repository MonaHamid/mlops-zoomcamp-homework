import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

@transformer
def train_model(df: pd.DataFrame, *args, **kwargs):
    # Use pickup and dropoff separately (do not combine!)
    features = ['PULocationID', 'DOLocationID', 'trip_distance']
    target = 'duration'

    # Convert to dict
    dicts = df[features].to_dict(orient='records')

    # Fit DictVectorizer
    dv = DictVectorizer()
    X_train = dv.fit_transform(dicts)
    y_train = df[target].values

    # Fit model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Print intercept
    print(f" Intercept: {model.intercept_}")
    y_pred = model.predict(X_train)
    rmse = np.sqrt(mean_squared_error(y_train, y_pred))
    print(f" RMSE: {rmse:.2f}")

    return model, dv

