FROM python:3.7-slim

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY ./src /app
WORKDIR /app

EXPOSE 5000
CMD ["python3", "main.py"]
