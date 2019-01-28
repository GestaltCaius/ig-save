FROM python:3.7-alpine

COPY requirements.txt /
RUN pip3 install --no-cache-dir -r /requirements.txt

COPY src/ /app
WORKDIR /app

CMD ["python3", "main.py"]