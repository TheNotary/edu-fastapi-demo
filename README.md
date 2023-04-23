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


Invoke the app's endpoints:
```
# Simple type validated endpoint
curl http://127.0.0.1:8000/?name=john

$ curl -XPOST -H "Content-Type: application/json" http://127.0.0.1:8000/ml \
  -d '{"input_data": "This is a pretty neat FastAPI demo that uses an ML model to perform the task of sentiment analysis."}'
{"label":"NEGATIVE","score":0.7003686428070068,"input_data":"This is a pretty neat FastAPI demo that uses an ML model to perform the task of sentiment analysis."}
```


## Docker stuff

```
docker build . -t edu-fastapi-demo
docker run -it -p 8000:8000 edu-fastapi-demo
```



## References

- Hugging Face transformer package manager for ML models: https://www.youtube.com/watch?v=QEaBAZQCtwE
- Transformers docs: https://huggingface.co/docs/transformers/installation
- I think ChatGPT-4 stubbed out the FastAPI syntax per: Write a hello world application in FastAPI that shows off it's inbuilt data validation.
