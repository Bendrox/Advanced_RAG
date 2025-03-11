from langchain_chroma import Chroma
import os
from chromadb import PersistentClient
from chromadb.config import Settings

def input_chunks_chromasdb(chunks_dict:dict, nom_source:str, embedding_model, emb_model_name :str,chroma_db_path:str, chunk_strat:str):
    """Input chunks dans une base vectorielle ChromaDB à partir d'un dict.  

    Args:
        chunks_dict (dict): output of chunker_1_v1_step_2
        nom_source (str): exemple: nom de directive UE
        emb_model_name: @@@@@                                   
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
    #global chroma_db_art
    chroma_db_art = Chroma.from_texts(
        texts=texts,
        metadatas=metadatas,
        # old version: persist_directory=f"{chemin}/Vector_store_{nom_source}_{chunk_strat}",
        persist_directory= chroma_db_path,
        embedding=embedding_model,
        collection_name= f"Chunk_strat_{chunk_strat}_{emb_model_name}",
        collection_metadata = {
        "hnsw:space": "cosine",          
        "hnsw:construction_ef": 200, # Nbr de voisins explorés lors de l'ajout
        "hnsw:M": 16   }             # Nbr de co par vecteur
    )
    return chroma_db_art


def input_chunks_chromasdb(chunks_dict:dict, nom_source:str, embedding_model, emb_model_name :str,chroma_db_path:str, chunk_strat:str):
    """Input chunks dans une base vectorielle ChromaDB à partir d'un dict.  

    Args:
        chunks_dict (dict): output of chunker_1_v1_step_2
        nom_source (str): exemple: nom de directive UE
        emb_model_name: @@@@@                                   
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
    #global chroma_db_art
    chroma_db_art = Chroma.from_texts(
        texts=texts,
        metadatas=metadatas,
        # old version: persist_directory=f"{chemin}/Vector_store_{nom_source}_{chunk_strat}",
        persist_directory= chroma_db_path,
        embedding=embedding_model,
        collection_name= f"Chunk_strat_{chunk_strat}_{emb_model_name}",
        collection_metadata = {
        "hnsw:space": "cosine",          
        "hnsw:construction_ef": 200, # Nbr de voisins explorés lors de l'ajout
        "hnsw:M": 16   }             # Nbr de co par vecteur
    )
    return chroma_db_art

def source_exists_in_chroma(chemin:str, chunk_stratégie, source_name, emb_model_name, embedding_model):
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
         collection_name= f"Chunk_strat_{chunk_stratégie}_{emb_model_name}" , 
         embedding_function=embedding_model)
 
     retriever = chroma_db.as_retriever()
     docs = retriever.invoke("test", filter={"source": source_name})
 
     return len(docs) > 0
 
def source_exists_in_chroma_v2(chemin:str, chunk_strat, source_name, emb_model_name, embedding_model):
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
         #collection_name= f"Chunk_strat_{chunk_stratégie}_{emb_model_name}" , 
         embedding_function=embedding_model)
 
     retriever = chroma_db.as_retriever()
     docs = retriever.invoke("test", filter={"source": source_name,"Chunk_strat":chunk_strat, "Embeding_model":emb_model_name })
 
     return len(docs) > 0

def print_res(results:list):
    """Print output of similarity_search_with_relevance_scores

    Args:
        results (list of articles)
    """
    for doc, score in results:
        print(f"\n *** Simil={score:.3f}, {doc.metadata} : {doc.page_content} ")
        
        
        
def input_chunks_chromasdb_v2(chunks_dict:dict, nom_source:str, embedding_model, emb_model_name :str,chroma_db_path:str, chunk_strat:str):
    """Input chunks dans une base vectorielle ChromaDB à partir d'un dict.  
    Approche orientée metadonnées
    Args:
        chunks_dict (dict): output of chunker_1_v1_step_2
        nom_source (str): exemple: nom de directive UE
        emb_model_name:                                    
        embedding_model (AzureOpenAI): 
        chemin (str): local enregistre

    Returns:
        Vector database: chroma_db
    """
    texts = list(chunks_dict.values())  # contenu des articles
    metadatas = [
        {"source": nom_source, "article": article_id, "Chunk_strat":chunk_strat, "Embeding_model":emb_model_name }
        for article_id in chunks_dict.keys()
    ]
    #global chroma_db_art
    chroma_db_art = Chroma.from_texts(
        texts=texts,
        metadatas=metadatas,
        # old version: persist_directory=f"{chemin}/Vector_store_{nom_source}_{chunk_strat}",
        persist_directory= chroma_db_path,
        embedding=embedding_model,
        collection_metadata = {
        "hnsw:space": "cosine",          
        "hnsw:construction_ef": 200, # Nbr de voisins explorés lors de l'ajout
        "hnsw:M": 16   }             # Nbr de co par vecteur
    )
    return chroma_db_art

def load_existing_chromasdb(db_path, embedding_model):
    chroma_db = Chroma(
        persist_directory=db_path,
        embedding_function=embedding_model
    )
    return chroma_db