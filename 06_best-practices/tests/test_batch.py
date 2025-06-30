import pandas as pd
from datetime import datetime
from batch import prepare_data

# Helper function to build datetime objects
def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def test_prepare_data():
    # Sample input data
    data = [
        (None, None, dt(1, 1), dt(1, 10)),            # 9 min → ✅
        (1, 1, dt(1, 2), dt(1, 10)),                  # 8 min → ✅
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),         # 59 sec → 0.98 min → ❌
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),             # 1441 min → ❌
    ]
    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    categorical = ['PULocationID', 'DOLocationID']

    # Run transformation
    result_df = prepare_data(df, categorical)

    # Expected output
    expected_data = [
        ('-1', '-1', 9.0),
        ('1', '1', 8.0)
    ]
    expected_df = pd.DataFrame(expected_data, columns=['PULocationID', 'DOLocationID', 'duration'])

    # Compare result to expected
    pd.testing.assert_frame_equal(
        result_df[['PULocationID', 'DOLocationID', 'duration']].reset_index(drop=True),
        expected_df
    )
