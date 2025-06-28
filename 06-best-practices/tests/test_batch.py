from datetime import datetime
import pandas as pd

# Import the prepare_data function from your batch.py script
# Make sure your batch.py is in the root of your project, next to the 'tests' folder
from batch import prepare_data 

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def test_prepare_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ["PULocationID", "DOLocationID", "tpep_pickup_datetime", "tpep_dropoff_datetime"]
    df = pd.DataFrame(data, columns=columns)

    categorical = ["PULocationID", "DOLocationID"]
    df_prepared = prepare_data(df, categorical)

    #  PRINT THE LENGTH
    print(f"\nLength of prepared DataFrame: {len(df_prepared)}")

    
    assert len(df_prepared) == expected_rows

    
