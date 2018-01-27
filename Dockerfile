#python 2.7 Compact 
#Compatible with App Engine standard environment APIs
#FROM gcr.io/google_appengine/python-compat-multicore
FROM gcr.io/google-appengine/python

#Python 2.7 & 3.4 image, but not compatible with App Engine standard environment APIs
#FROM gcr.io/google_appengine/python
#RUN apt-get update && apt-get install --no-install-recommends -y -q wget unzip python2.7-dev Cython libgcrypt11-dev gcc
RUN apt-get update && apt-get install -y wget unzip python2.7-dev Cython
#RUN pip install --upgrade pip virtualenv

# download google_appengine sdk
#ENV GOOGLE_APPENGINE_SDK google_appengine
#ENV GOOGLE_APPENGINE_VERSION 1.9.38
#WORKDIR /google
#RUN wget --trust-server-names https://storage.googleapis.com/appengine-sdks/featured/$GOOGLE_APPENGINE_SDK\_$GOOGLE_APPENGINE_VERSION.zip
#RUN unzip $GOOGLE_APPENGINE_SDK\_$GOOGLE_APPENGINE_VERSION.zip
#ENV PATH /google/$GOOGLE_APPENGINE_SDK:$PATH
#ENV PYTHONPATH /google/$GOOGLE_APPENGINE_SDK:/google/$GOOGLE_APPENGINE_SDK/lib/:/google/$GOOGLE_APPENGINE_SDK/lib/yaml:/google/$GOOGLE_APPENGINE_SDK/lib/yaml/lib:$PYTHONPATH

# default python 2.7
RUN virtualenv /env

## setup virtual env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

## Python 2 (implicit)
#RUN virtualenv $VIRTUAL_ENV
### Python 3
## RUN virtualenv /env -p python3.4
### Python 2 (explicit)
##RUN virtualenv /env -p python2.7

## Set virtualenv environment variables. This is equivalent to running
#source $VIRTUAL_ENV/bin/activate

ADD . /app/
#WORKDIR /app
#ENV PORT 8080
#EXPOSE 22 8080

#ADD requirements.txt /app/
RUN pip install numpy
RUN pip install -r requirements.txt
#CMD gunicorn -b :$PORT main:app
CMD gunicorn -b :$PORT -c gunicorn.conf.py main:app
