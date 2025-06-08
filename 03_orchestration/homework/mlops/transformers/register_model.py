import mlflow
import mlflow.sklearn

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def transform(inputs: dict, **kwargs):
    model = inputs['model']
    dv = inputs['dv']

    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("nyc_taxi_march")

    with mlflow.start_run():
        mlflow.sklearn.log_model(model, artifact_path="model")
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_metric("intercept", model.intercept_)

        print("Model logged to MLflow")

    return {}