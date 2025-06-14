FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

WORKDIR /app

# Only copy the script (model.bin already exists in base image)
COPY batch.py .

RUN pip install pandas pyarrow scikit-learn


ENTRYPOINT ["python", "batch.py"]

