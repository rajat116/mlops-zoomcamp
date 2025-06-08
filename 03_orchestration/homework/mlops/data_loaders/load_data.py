import pandas as pd
from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_data(*args, **kwargs):
    df = pd.read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet')
    print("Loaded records:", len(df))
    return df