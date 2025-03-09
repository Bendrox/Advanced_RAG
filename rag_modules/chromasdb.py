from langchain_chroma import Chroma
import os
from chromadb import PersistentClient
from chromadb.config import Settings

def input_chunks_chromasdb(chunks_dict:dict, nom_source:str, embedding_model, chemin:str, chunk_version:str):
    """Input chunks dans une base vectorielle ChromaDB à partir d'un dict.
    Fonction pour simple chunk par article  

    Args:
        chunks_dict (dict): output of chunker_1_v1_step_2
        nom_source (str): exemple: nom de directive UE
        embedding_model (AzureOpenAI): 
        chemin (str): local enregistre

    Returns:
        Vector database: chroma_db
    """
    texts = list(chunks_dict.values())  # contenu des articles
    metadatas = [
        {"source": nom_source, "article": article_id}
        for article_id in chunks_dict.keys()
    ]
    global chroma_db
    chroma_db = Chroma.from_texts(
        texts=texts,
        metadatas=metadatas,
        persist_directory=f"{chemin}_{nom_source}_{chunk_version}",
        embedding=embedding_model,
        collection_metadata = {
        "hnsw:space": "cosine",          
        "hnsw:construction_ef": 200, # Nbr de voisins explorés lors de l'ajout
        "hnsw:M": 16   }             # Nbr de co par vecteur
    )
    return chroma_db


def source_exists_in_chroma(chemin, source_name, embedding_model):
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
     docs = retriever.invoke("tsst", filter={"source": source_name})
 
     return len(docs) > 0
 


def load_existing_chromasdb(db_path, embedding_model):
    chroma_db = Chroma(
        persist_directory=db_path,
        embedding_function=embedding_model
    )
    return chroma_db


def print_res(results:list):
    """Print output of similarity_search_with_relevance_scores

    Args:
        results (list of articles)
    """
    for doc, score in results:
        print(f"\n *** Simil={score:.3f}, {doc.metadata} : {doc.page_content} ")