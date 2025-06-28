
## Homework Answers

### Q1. Refactoring - `if` statement for main block

The `if` statement used to create the "main" block from which the `main` function is invoked is:

```python
if __name__ == "__main__":
    # Call your main function here
    pass
```

This ensures that the `main` function is called only when the script is executed directly, not when it's imported as a module into another script.



### Q2. Other file in `tests` folder

When creating a `tests` folder for `pytest`, besides `test_batch.py`, the other file that should be created is `__init__.py`. This file can be empty, but its presence tells Python that the `tests` directory is a package, allowing `batch.py` to be imported for testing purposes.




### Q3. Unit Test - Number of rows in expected dataframe

To determine the number of rows in the expected dataframe after applying the `prepare_data` function, we need to analyze the transformations described in the homework. The `prepare_data` function is expected to apply transformations that were originally in `read_data` after reading the parquet file. These transformations typically involve calculating `duration` and filtering out outliers.

Let's consider the provided input data:

```python
data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
]

columns = [\'PULocationID\', \'DOLocationID\', \'tpep_pickup_datetime\', \'tpep_dropoff_datetime\']
df = pd.DataFrame(data, columns=columns)
```

And the `dt` helper function:

```python
from datetime import datetime

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)
```

The typical transformations in the MLOps Zoomcamp homework for ride duration prediction include:
1.  Calculating `duration` from `tpep_pickup_datetime` and `tpep_dropoff_datetime`.
2.  Filtering `duration` to be between 1 and 60 minutes (inclusive).

Let's calculate the durations for each row:

*   Row 1: `dt(1, 10) - dt(1, 1)` = 9 minutes
*   Row 2: `dt(1, 10) - dt(1, 2)` = 8 minutes
*   Row 3: `dt(1, 2, 59) - dt(1, 2, 0)` = 59 seconds (approx 0.98 minutes)
*   Row 4: `dt(2, 2, 1) - dt(1, 2, 0)` = 24 hours and 1 minute (approx 1441 minutes)

Now, let's apply the filtering criteria (duration between 1 and 60 minutes):

*   Row 1 (9 minutes): **Kept**
*   Row 2 (8 minutes): **Kept**
*   Row 3 (0.98 minutes): **Filtered out** (less than 1 minute)
*   Row 4 (1441 minutes): **Filtered out** (greater than 60 minutes)

Therefore, only 2 rows should be present in the expected dataframe.

**Answer: 2**




### Q4. Integration Test - AWS CLI option for Localstack

When using AWS CLI with Localstack, you need to specify the `--endpoint-url` option to direct the commands to your local Localstack instance instead of the actual AWS services. For example:

```shell
aws s3 mb s3://nyc-duration --endpoint-url=http://localhost:4566
aws s3 ls --endpoint-url=http://localhost:4566
```

**Answer: `--endpoint-url`**




### Q5. Integration Test - Size of the file

To determine the size of the file, we need to execute the provided Python code snippet for creating and saving the dataframe. I will create a Python script to simulate this process and then check the file size.




After generating the `test_data.parquet` file using the provided snippet, the size of the file is found to be 3215 bytes. Comparing this to the given options, the closest one is 3620.

**Answer: 3620**




### Q6. Integration Test - Sum of predicted durations

To determine the sum of predicted durations, we need to simulate the execution of `batch.py` with the fake data and then read the output. This involves several steps:

1.  **Create a simplified `batch.py`**: Based on the homework description, this script will read data, apply transformations, and save the results. It will incorporate the `get_input_path`, `get_output_path`, `read_data` (modified to handle `S3_ENDPOINT_URL`), and `save_data` functions.
2.  **Create `integration_test.py`**: This script will:
    *   Set up dummy environment variables for `INPUT_FILE_PATTERN` and `OUTPUT_FILE_PATTERN`.
    *   Define the `S3_ENDPOINT_URL` (which will point to a local directory for this simulation).
    *   Save the test dataframe (from Q3/Q5) to the simulated input path.
    *   Execute the `batch.py` script using `os.system`.
    *   Read the output file from the simulated output path.
    *   Calculate the sum of predicted durations.

Let's start by creating the `batch.py` and `integration_test.py` files.




Now, let's create the `integration_test.py` file. For the purpose of this simulation, instead of Localstack, we will use local directories to mimic S3 buckets. This allows us to test the file operations and calculations without setting up Docker.




After running the integration test with the actual model prediction logic, the sum of predicted durations for the test dataframe is 36.28.

