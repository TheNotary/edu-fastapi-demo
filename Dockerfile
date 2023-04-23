FROM python:3.11

RUN mkdir /app
WORKDIR /app

# Install deps
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY app.py /app/app.py

CMD uvicorn app:app --reload --host 0.0.0.0 --port 8000
