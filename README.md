# FastAPI Demo

This is a quick demo to see how leveraging a simple ML pipeline and exposing it over a web API works.


## Setup for local development

```
python -m venv .env
source .env/bin/activate
# For window use this instead :)
# .\.env\Scripts\activate

pip install -r requirements.txt
```


## Run Locally

Run the server:

```
uvicorn app:app --reload --host 192.168.1.28 --port 8000
```

Invoke the app's endpoints:
```
$ MSG='This is a pretty neat FastAPI demo that uses an ML model to perform the task of sentiment analysis.'
$ curl -XPOST -H "Content-Type: application/json" http://127.0.0.1:8000/ml \
  -d "{\"input_data\": \"${MSG}\"}"
{"label":"NEGATIVE","score":0.7003686428070068,"input_data":"This is a pretty neat FastAPI demo that uses an ML model to perform the task of sentiment analysis."}
```


## Docker stuff

```
docker build . -t edu-fastapi-demo
docker run -it -p 8000:8000 edu-fastapi-demo
```


## References

- Intro to HuggingFace's Transformer's package manager/ framework for working with ML models: https://www.youtube.com/watch?v=QEaBAZQCtwE
- Transformers docs: https://huggingface.co/docs/transformers/installation
- Online book on FastAPI: https://fastapi.tiangolo.com/tutorial/first-steps/
- Handy FastAPI prompts (ChatGPT-4):
  - Write a hello world application in FastAPI that shows off it's inbuilt data validation.
  - How can I use pydantic and FastAPI to build an endpoint that will respond to the below curl with a validation error that input_data was not long enough.  `curl -XPOST 127.0.0.1:8000/ml -d '{"input_data": ""}'`
  - https://chat.openai.com/share/4ae644fe-0168-4ff5-8179-b3fd2f56e18c
