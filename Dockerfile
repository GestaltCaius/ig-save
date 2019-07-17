#FROM python:3.7
FROM joyzoursky/python-chromedriver:3.7-alpine3.8-selenium

RUN apk add --update --no-cache g++ gcc libxslt-dev

COPY requirements.txt /
RUN pip install -r /requirements.txt

#RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
#RUN tar xjf phantomjs-2.1.1-linux-x86_64.tar.bz2

COPY ./src /app
WORKDIR /app

#ENV PATH="/phantomjs-2.1.1-linux-x86_64/bin/:${PATH}"
ENV FLASK_APP main.py
ENV FLASK_DEBUG 1

CMD flask run --host 0.0.0.0 --port $PORT
