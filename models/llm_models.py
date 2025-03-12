
from langchain_openai import AzureChatOpenAI
#from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain_openai import AzureOpenAIEmbeddings

from dotenv import load_dotenv
import os
load_dotenv()


llm_4omini = AzureChatOpenAI(
    azure_deployment="gpt-4o-mini",  # or your deployment
    api_version="2025-01-01-preview",  # or your api version
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

llm_41_mini = AzureChatOpenAI(
    azure_deployment="gpt-4o-mini",  # or your deployment
    api_version="2025-01-01-preview",  # or your api version
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)


def llm_stream_response(model:str, prompt):
    "Envoi au llm et affiche réponse en direct"
    for chunk in model.stream(prompt):
        print(chunk.content, end="", flush=True)
        