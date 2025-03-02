from langchain_chroma import Chroma
import os
from chromadb import PersistentClient
from chromadb.config import Settings


def input_data_chromasdb(chunks_dict, nom_source, embedding_model, chemin):
    texts = list(chunks_dict.values())  # contenu des articles
    metadatas = [
        {"source": nom_source, "article": article_id}
        for article_id in chunks_dict.keys()
    ]
    chroma_db = Chroma.from_texts(
        texts=texts,
        metadatas=metadatas,
        persist_directory=chemin,
        embedding=embedding_model
    )
    return chroma_db



def load_existing_chromasdb(db_path, embedding_model):
    chroma_db = Chroma(
        persist_directory=db_path,
        embedding_function=embedding_model
    )
    return chroma_db