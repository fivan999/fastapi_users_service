FROM python:3.11.9-alpine
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt