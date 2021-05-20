FROM python:3.8

RUN mkdir /app
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
COPY . .

CMD gunicorn server.wsgi:application --bind 0.0.0.0:8000