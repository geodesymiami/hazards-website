FROM continuumio/miniconda3

RUN conda install boto3 botocore gdal matplotlib pandas pillow pymysql rasterio

WORKDIR /processing

COPY . /processing

CMD ["python", "pipeline.py"]