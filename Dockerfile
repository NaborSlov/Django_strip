FROM python:3.11-slim

WORKDIR /django_strip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ./manage.py runserver 0.0.0.0:8000


