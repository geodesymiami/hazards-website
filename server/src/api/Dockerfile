FROM terrillo/python3flask:latest

# STATIC paths for file.
# Don't use flask static. Nginx is your friend
ENV STATIC_URL /static
ENV STATIC_PATH /app/static

ENV WORKDIR src/api
ENV COMMON_DIR src/common
ENV REQUIREMENTS $WORKDIR/requirements.txt

WORKDIR app
ADD $REQUIREMENTS requirements.txt

# Install requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

## Place your flask application on the server
COPY $WORKDIR .
COPY $COMMON_DIR common

RUN export PYTHONPATH="$PYTHONPATH:$COMMON_DIR"

# NGINX setup
COPY $WORKDIR/nginx.sh /nginx.sh
RUN chmod +x /nginx.sh

ENV PYTHONPATH=/app

ENTRYPOINT ["/nginx.sh"]
CMD ["/start.sh"]

EXPOSE 80 443




#FROM continuumio/miniconda3
#
#EXPOSE 5000
#
#ENV WORKDIR src/api
#ENV COMMON_DIR src/common
#ENV REQUIREMENTS $WORKDIR/requirements.txt
#
#WORKDIR app
#
#ADD $REQUIREMENTS requirements.txt
#RUN conda install --yes --file requirements.txt
#
#COPY $WORKDIR .
#COPY $COMMON_DIR common
#
#RUN export PYTHONPATH="$PYTHONPATH:$COMMON_DIR"
#
#CMD ["python", "main.py"]