from typing import Dict
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def transform(df: pd.DataFrame, **kwargs) -> Dict:
    df['PU'] = df['PULocationID']
    df['DO'] = df['DOLocationID']

    train_dicts = df[['PU', 'DO']].to_dict(orient='records')
    y_train = df['duration'].values

    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts)

    model = LinearRegression()
    model.fit(X_train, y_train)

    print("Model intercept:", round(model.intercept_, 2))

    return {
        'model': model,
        'dv': dv
    }