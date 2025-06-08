import pandas as pd

df = pd.read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet')

print("Loaded records:", len(df))

df

