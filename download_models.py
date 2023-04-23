from transformers import AutoTokenizer, AutoModel

def download_and_cache_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

# List the models you want to cache
models_to_cache = [
    "distilbert-base-uncased-finetuned-sst-2-english"
]

for model_name in models_to_cache:
    download_and_cache_model(model_name)
