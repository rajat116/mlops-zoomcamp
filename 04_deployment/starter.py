#!/usr/bin/env python
# coding: utf-8
import pickle
import os
import pandas as pd
import numpy as np
import sys
import boto3

year = int(sys.argv[1])
month = int(sys.argv[2])

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

#year = 2023
#month = 3

input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
output_file = f'preds_{year:04d}-{month:02d}.parquet'

df = read_data(input_file)

dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)

std_pred = np.std(y_pred)
print(f"Standard Deviation of Predicted Duration: {std_pred:.2f}")

df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

df_result = pd.DataFrame()
df_result['ride_id'] = df['ride_id']
df_result['predicted_duration'] = y_pred

df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)

# Upload to S3
bucket = os.getenv('S3_BUCKET')
s3_path = f'predictions/{output_file}'
s3 = boto3.client('s3')
s3.upload_file(output_file, bucket, s3_path)
print(f"✅ Uploaded to s3://{bucket}/{s3_path}")
