from langchain_text_splitters import RecursiveCharacterTextSplitter
from data_pipelines.token_counter import count_tokens
import re
import numpy as np
from langchain_core.documents import Document

def chunker_1(input_data_to_chunk: str ) -> dict:
    """Optimal chunker by article tested and approved on AML5, CRR and DSP2 

    Args:
        input_data_to_chunk (str): texte entrée a chunker apres conversion de pdf

    Returns:
        dict: of chunks
    """
    article_splitter = RecursiveCharacterTextSplitter(separators= ["Article"],chunk_size= 300, chunk_overlap=0)
    chunks= article_splitter.split_text(input_data_to_chunk)
    def ajouter_espace_article(texte): return re.sub(r'(Article\s+\d+)\s*([^\d\s])', r'\1  \2', texte)
    chunks=[ajouter_espace_article(i) for i in chunks]
    chunks_dic = {item[:11].strip(): item[10:].lstrip() for item in chunks}
    return chunks_dic

def chunker_2(input_data_to_chunk: str) -> list:
    """Chunker by "CHAPITRE", "SECTION", "Article".
    # Attention résultats variables !
    Args:
        input_data_to_chunk: texte entrée a chunker apres conversion de pdf

    Returns:
        list: of chunks
    """
    article_splitter = RecursiveCharacterTextSplitter(
    separators= ["CHAPITRE", "SECTION", "Article"],
    chunk_size= 100,
    chunk_overlap=0),
    chunks= article_splitter.split_text(input_data_to_chunk)
    return chunks

def chunker_3(chunks_UE_dict: dict, Directive_source:str):
    """
    Dict d’articles -> liste objects Document avec métadonnées (Directive_source , N°article)

    Args:
        chunks_UE_dict (dict): Dictionnaire id sont articles et les clés contenus. 
        Directive_source (str): Nom ou référence de la directive UE. 

    Returns:
        list: Document(id='1', metadata={'Directive_source': 'DPS2', 'N°article ': 'pre'}, page_content='mier Objet)
    """
    documents = []
    for article_key, article_content in chunks_UE_dict.items():
        doc = Document(
            page_content=article_content.lstrip(), 
            metadata={"Directive_source": Directive_source , "N°article ": article_key[7:].strip()}, 
            id=len(documents) + 1  # nombre de documents déjà créés 
        )
        documents.append(doc)
    return documents


    
def chunk_stat_token(your_chunks):
    """Produit des stats sur le nombre de tokens par chunks. 
    Pour but d'améliorer les performances 

    Args:your_chunks
    """
    chunk_lengths = [count_tokens(chunk) for chunk in your_chunks]
    print("Nombre de chunks:", len(chunk_lengths))
    print("Nombre de token des chunks:", chunk_lengths)
    print("Nombre de token moyen par chunk :", np.mean(chunk_lengths))
    print("Nombre de token max par chunk :", np.max(chunk_lengths))
    print("Nombre de token min par chunk :", np.min(chunk_lengths))

