FROM continuumio/miniconda3

EXPOSE 5000

ENV WORKDIR src/api
ENV COMMON_DIR src/common
ENV REQUIREMENTS $WORKDIR/requirements.txt

WORKDIR app

ADD $REQUIREMENTS requirements.txt
RUN conda install --yes --file requirements.txt

COPY $WORKDIR .
COPY $COMMON_DIR common

RUN export PYTHONPATH="$PYTHONPATH:$COMMON_DIR"

CMD ["python", "endpoints.py"]