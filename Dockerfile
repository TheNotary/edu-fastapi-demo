FROM python:3.11

RUN mkdir /app
WORKDIR /app

# Set up the cache directory for Hugging Face Transformers
ENV TRANSFORMERS_CACHE=/app/transformers_cache
RUN mkdir -p $TRANSFORMERS_CACHE

# Install deps
COPY requirements.txt /app
RUN pip install -r requirements.txt

# TODO: Lookup/ develop best practice for dealing with model versions
# Cache sentiment-analysis
# RUN python -c "from transformers import pipeline; print(pipeline('sentiment-analysis')('I love you'))"
COPY download_models.py /app
RUN python download_models.py

COPY app.py /app/app.py

CMD uvicorn app:app --reload --host 0.0.0.0 --port 8000
