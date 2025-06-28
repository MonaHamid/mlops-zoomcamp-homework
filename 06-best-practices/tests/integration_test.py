import pandas as pd
from datetime import datetime
import os
import shutil
import s3fs # Make sure to install this: pip install s3fs

# Function to generate datetime objects
def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

# Define S3 bucket and paths
S3_ENDPOINT_URL = "http://localhost:4566" # This is the correct LocalStack endpoint
INPUT_BUCKET = "nyc-duration"
OUTPUT_BUCKET = "nyc-duration"
INPUT_PREFIX = "in"
OUTPUT_PREFIX = "out"

# Set environment variables for batch.py
os.environ["INPUT_FILE_PATTERN"] = f"s3://{INPUT_BUCKET}/{INPUT_PREFIX}/{{year:04d}}-{{month:02d}}.parquet"
os.environ["OUTPUT_FILE_PATTERN"] = f"s3://{OUTPUT_BUCKET}/{OUTPUT_PREFIX}/{{year:04d}}-{{month:02d}}.parquet"
os.environ["S3_ENDPOINT_URL"] = S3_ENDPOINT_URL

# Create an S3 filesystem object
s3 = s3fs.S3FileSystem(client_kwargs={'endpoint_url': S3_ENDPOINT_URL} )

# Clean up previous runs in S3 (optional, but good for testing)
# Note: This requires the bucket to exist. You might need to create it manually
# or add bucket creation logic here if it's not guaranteed to exist.
try:
    # Ensure the bucket exists
    if not s3.exists(INPUT_BUCKET):
        s3.mkdir(INPUT_BUCKET)
    if not s3.exists(OUTPUT_BUCKET):
        s3.mkdir(OUTPUT_BUCKET)

    # Remove previous test data
    s3.rm(f"{INPUT_BUCKET}/{INPUT_PREFIX}", recursive=True)
    s3.rm(f"{OUTPUT_BUCKET}/{OUTPUT_PREFIX}", recursive=True)
except Exception as e:
    print(f"Could not clean S3 paths (they might not exist yet): {e}")

# Create the test dataframe (from Q3/Q5)
data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
]

columns = ["PULocationID", "DOLocationID", "tpep_pickup_datetime", "tpep_dropoff_datetime"]
df_input = pd.DataFrame(data, columns=columns)

# Save the test dataframe to the simulated S3 input path
input_s3_path = f"s3://{INPUT_BUCKET}/{INPUT_PREFIX}/2023-01.parquet"
df_input.to_parquet(
    input_s3_path,
    engine="pyarrow",
    compression=None,
    index=False,
    storage_options={'client_kwargs': {'endpoint_url': S3_ENDPOINT_URL}}
)

print(f"Input file saved to S3: {input_s3_path}")

# Execute batch.py
print("Running batch.py...")
# Ensure batch.py is in the same directory or its path is correct
os.system("python3 batch.py") 
print("batch.py finished.")

# Read the output file from S3 and calculate sum of predicted durations
output_s3_path = f"s3://{OUTPUT_BUCKET}/{OUTPUT_PREFIX}/2023-01.parquet"
df_output = pd.read_parquet(
    output_s3_path,
    storage_options={'client_kwargs': {'endpoint_url': S3_ENDPOINT_URL}}
)

sum_predicted_durations = df_output["predicted_duration"].sum()

print(f"Sum of predicted durations: {sum_predicted_durations}")

# Assert the result
expected_sum = 36.27725045203073 # Use the exact value for comparison
assert abs(sum_predicted_durations - expected_sum) < 1e-9, \
    f"Expected sum {expected_sum}, but got {sum_predicted_durations}"

print("Integration test passed!")
