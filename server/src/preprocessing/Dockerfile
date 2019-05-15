FROM continuumio/miniconda3

# Should be /home/amelung/hazards on Jetstream
ENV WORKDIR src/preprocessing
ENV COMMON_DIR src/common
ENV RESOURCES_DIR $WORKDIR/resources
ENV REQUIREMENTS $RESOURCES_DIR/requirements.txt

WORKDIR dataprocessing

ADD $REQUIREMENTS requirements.txt
RUN conda install --yes --file requirements.txt

COPY $WORKDIR .
COPY $COMMON_DIR common
COPY $RESOURCES_DIR resources

RUN export PYTHONPATH="$PYTHONPATH:$COMMON_DIR"

CMD ["python", "pipeline.py"]