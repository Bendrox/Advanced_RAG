from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
import os


emb_3_large = AzureOpenAIEmbeddings(
    model="text-embedding-3-large",
    azure_endpoint=os.getenv('Azure_OpenAI_emb_3_large_azure_endpoint'),
    openai_api_key=os.getenv('Azure_OpenAI_emb_3_large_api_key'),
    openai_api_version="2023-05-15",
    chunk_size=1000
)

def funct_embedding(input):
    """
    embedding d'un texte en utilisant le modèle `text-embedding-3-large`.

    Args:
        input_text (str): Le texte pour lequel générer l'embedding.

    Returns:
        list[float]: Vecteur embedding sous forme de liste de flottants.
    """
    emb = emb_3_large.embed_query(input)
    return emb