# FastAPI Demo

This is a quick demo to see how leveraging a simple ML pipeline and exposing it over a web API works.


## Setup for local development

```
python -m venv .env
source .env/bin/activate

pip install -r requirements.txt
```


## Run Locally

Run the server:

```
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Send some phrase to the server to check it's sentiment:

```
curl localhost:8000 -d '{}'
```


## References

- Hugging Face transformer package manager for ML models: https://www.youtube.com/watch?v=QEaBAZQCtwE
- Transformers docs: https://huggingface.co/docs/transformers/installation
- I think ChatGPT-4 stubbed out the FastAPI syntax per: Write a hello world application in FastAPI that shows off it's inbuilt data validation.
