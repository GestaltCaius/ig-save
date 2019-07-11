FROM python:3.7-slim

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY ./src /app
WORKDIR /app

ENV FLASK_APP main.py
ENV FLASK_DEBUG 1

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
