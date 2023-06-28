# FastAPI Demo

This is an education demo showing how to leverage various datascience projects.  Everything is exposed over a pythong web API framework called FastAPI.


### File Structure

This project contains demonstration code for various aspects of datascience.  To keep things from getting confusing, each concept is modularized; each concept gets it's own folder where *most* of the related code lives.  The below diagram shows the important files if you were concerned with, say, how the 'basics' demo works (`/basics`).

```bash
├── static/basics/
│      ├── sentiment_router.py # controller & misc. code for doing the demo
│      ├── index.html          # HTML code for the index page of the demo
│      ├── custom.css          # any styling for the demo
│      └── index.js            # any javascript involved in the demo
│
├── layout/
│      ├── _base.html          # The template that all pages follow
│      └── _navbar.html        # The navbar for the site
│
└── app.py                     # Entrypoint for the FastAPI app
```


## Setup for local development

```
python -m venv .env
source .env/bin/activate
# For window use this instead :)
# .\.env\Scripts\activate

pip install -r requirements.txt
```


## Manually Download Models

Some models download automatically at runtime, but some are loaded manually.

```
wget https://huggingface.co/TheBloke/WizardLM-30B-Uncensored-GGML/resolve/main/wizardlm-30b-uncensored.ggmlv3.q6_K.bin
```


## Run Locally

Run the server:

```
uvicorn app:app --reload --host 192.168.1.28 --port 8000
```

Invoke one of the app's endpoints over curl:
```
$ MSG='This is a pretty neat FastAPI demo that uses an ML model to perform the task of sentiment analysis.'
$ curl -XPOST -H "Content-Type: application/json" http://127.0.0.1:8000/ml \
  -d "{\"input_data\": \"${MSG}\"}"
{"label":"NEGATIVE","score":0.7003686428070068,"input_data":"This is a pretty neat FastAPI demo that uses an ML model to perform the task of sentiment analysis."}
```


## Docker Stuff

Note:  Not currently maintained due to how my current ML infrastructure is setup (windows machine =/).

```
docker build . -t edu-fastapi-demo
docker run -it -p 8000:8000 edu-fastapi-demo
```


## References

- Intro to HuggingFace's Transformer's package manager/ framework for working with ML models: https://www.youtube.com/watch?v=QEaBAZQCtwE
- Transformers docs: https://huggingface.co/docs/transformers/installation
- gpt4all: https://github.com/nomic-ai/gpt4all/tree/main/gpt4all-bindings/python
- [Wizard LM](https://github.com/abetlen/llama-cpp-python#high-level-api)
- Online book on FastAPI: https://fastapi.tiangolo.com/tutorial/first-steps/
- Handy FastAPI prompts (ChatGPT-4):
  - Write a hello world application in FastAPI that shows off it's inbuilt data validation.
  - How can I use pydantic and FastAPI to build an endpoint that will respond to the below curl with a validation error that input_data was not long enough.  `curl -XPOST 127.0.0.1:8000/ml -d '{"input_data": ""}'`
  - https://chat.openai.com/share/4ae644fe-0168-4ff5-8179-b3fd2f56e18c
