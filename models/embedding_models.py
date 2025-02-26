from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
import os


embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-large",
    azure_endpoint=os.getenv('Azure_OpenAI_emb_3_large_azure_endpoint'),
    openai_api_key=os.getenv('Azure_OpenAI_emb_3_large_api_key'),
    openai_api_version="2023-05-15",
    chunk_size=1000
)