FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

WORKDIR /app
COPY starter.py .

RUN pip install pandas pyarrow scikit-learn==1.5.0 boto3

ENTRYPOINT ["python", "starter.py"]
