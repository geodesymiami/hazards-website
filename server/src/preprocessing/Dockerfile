FROM continuumio/miniconda3

# Should be /home/amelung/hazards on Jetstream
ENV COMMON_DIR src/common
ENV REQUIREMENTS src/python_requirements.txt
ENV WORKDIR src/preprocessing

WORKDIR ${WORKDIR}

ADD $REQUIREMENTS $WORKDIR/requirements.py
RUN conda install --yes --file $WORKDIR/requirements.py
RUN export PYTHONPATH="$PYTHONPATH:$COMMON_DIR"


COPY $WORKDIR $WORKDIR
COPY src/common $WORKDIR/common

CMD ["pwd"]
CMD ["python", "src/preprocessing/pipeline.py"]