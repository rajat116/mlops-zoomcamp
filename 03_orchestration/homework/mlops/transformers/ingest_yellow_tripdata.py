import pandas as pd

url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet'
df = pd.read_parquet(url)
print("Loaded records:", len(df))

df
