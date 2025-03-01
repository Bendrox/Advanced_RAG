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


def source_exists_in_chroma(chemin, source_name, embedding_model) -> bool:
    """
    Vérifie si une source donnée existe déjà dans la base Chroma persistée.
    Args:
        chemin (str): Dossier de persistance de Chroma.
        source_name (str): Nom de la source à chercher dans les métadonnées.
        embedding_model: Modèle d'embedding utilisé pour initier Chroma.

    Returns: True si la source est déjà indexée, False sinon.
    """
    
    # Charge la base Chroma existante
    chroma_db = Chroma(
        persist_directory=chemin,
        embedding_function=embedding_model)

    retriever = chroma_db.as_retriever()
    docs = retriever.invoke("test", filter={"source": source_name})

    return len(docs) > 0

def load_existing_chromasdb(db_path, embedding_model):
    chroma_db = Chroma(
        persist_directory=db_path,
        embedding_function=embedding_model
    )
    return chroma_db