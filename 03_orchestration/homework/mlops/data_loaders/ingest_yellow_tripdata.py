import pandas as pd
from mage_ai.data_preparation.decorators import data_loader

@data_loader
def ingest_yellow_tripdata(**kwargs) -> pd.DataFrame:
    url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet'
    df = pd.read_parquet(url)
    print("Loaded records:", len(df))
    return df
