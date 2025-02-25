
from langchain_openai import AzureChatOpenAI
from langchain.embeddings import OpenAIEmbeddings, AzureOpenAIEmbeddings
from langchain.embeddings import AzureOpenAIEmbeddings

from dotenv import load_dotenv
import os


llm_4o = AzureChatOpenAI(
    azure_endpoint=os.getenv('Azure_OpenAI_OB_Endpoint'), 
    openai_api_version="2024-02-15-preview",
    model_name="gpt-4o",
    openai_api_key=os.getenv('Azure_OpenAI_OB_Key'), 
    openai_api_type="azure",
    temperature=0,
    deployment_name="gpt-4o-deploy")
    #streaming=True

llm_4omini = AzureChatOpenAI(
    azure_endpoint=os.getenv('Azure_OpenAI_OB_Endpoint_4mini'), 
    openai_api_version="2024-10-21",   
    model_name="gpt-4o-mini",
    openai_api_key=os.getenv('Azure_OpenAI_OB_Key_4mini'), 
    openai_api_type="azure",
    temperature=0,
    deployment_name="gpt4o-mini")
    #streaming=True
    
embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-large",
    azure_endpoint=os.getenv('Azure_OpenAI_emb_3_large_azure_endpoint'),
    openai_api_key=os.getenv('Azure_OpenAI_emb_3_large_api_key'),
    openai_api_version="2023-05-15",
    chunk_size=1000
)

def llm_stream_response(model:str, prompt):
    "Envoi au llm et affiche réponse en direct"
    for chunk in model.stream(prompt):
        print(chunk.content, end="", flush=True)
        