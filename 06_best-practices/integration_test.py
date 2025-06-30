# integration_test.py

import os
import pandas as pd
from datetime import datetime as dt

# === Set up environment variables ===
year = 2023
month = 1

os.environ['INPUT_FILE_PATTERN'] = 's3://nyc-duration/in/{year:04d}-{month:02d}.parquet'
os.environ['OUTPUT_FILE_PATTERN'] = 's3://nyc-duration/out/{year:04d}-{month:02d}.parquet'

input_file = os.getenv('INPUT_FILE_PATTERN').format(year=year, month=month)
output_file = os.getenv('OUTPUT_FILE_PATTERN').format(year=year, month=month)

options = {
    'client_kwargs': {
        'endpoint_url': 'http://localhost:4566'
    }
}

# === Create test dataframe (same as Q3) ===
data = [
    (None, None, dt(2023, 1, 1), dt(2023, 1, 10)),
    (1, 1, dt(2023, 1, 2), dt(2023, 1, 10)),
    (1, None, dt(2023, 1, 2, 0, 0), dt(2023, 1, 2, 0, 59)),
    (3, 4, dt(2023, 1, 2, 0), dt(2023, 1, 2, 1)),
]

columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df_input = pd.DataFrame(data, columns=columns)

# === Step 1: Save input to S3 ===
df_input.to_parquet(
    input_file,
    engine='pyarrow',
    compression=None,
    index=False,
    storage_options=options
)

# === Step 2: Run batch.py ===
ret_code = os.system(f'pipenv run python batch.py {year} {month}')
if ret_code != 0:
    raise RuntimeError("❌ batch.py failed to run")

# === Step 3: Read output from S3 ===
df_output = pd.read_parquet(output_file, storage_options=options)

# === Step 4: Check output ===
print("✅ Output predictions:")
print(df_output)

total_pred = df_output['predicted_duration'].sum()
print(f"\n✅ Total predicted duration: {total_pred:.2f}")