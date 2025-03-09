from langchain_text_splitters import RecursiveCharacterTextSplitter
from data_pipelines.token_counter import count_tokens
import re
import numpy as np
from langchain_core.documents import Document

# Chunker 1 : approche qui définit un chunk pour chaque article
def chunker_1_step_1(input_data_to_chunk: str ) -> list:
    """
    ### Optimal chunker by article when using chunk_stat_token() 
    
    Args:
        input_data_to_chunk (str): texte entrée a chunker apres conversion de pdf

    Returns:
        list: of chunks
    """
    article_splitter = RecursiveCharacterTextSplitter(
    separators=   ["Article"],
    chunk_size= 100, 
    chunk_overlap=0)
    chunks_list= article_splitter.split_text(input_data_to_chunk)
    return chunks_list

def chunker_1_step_2(beginning: int,end:int,chunks_dsp2_list:list) -> dict:
    """Step2: 
    ### Select beginning and end of a chunk + Add a space + Transform to dict
    ### Optimal using chunk_stat_token() 
    
    Args:
        beginning (int): _description_
        end (int): _description_
        chunks_dsp2_list (list): _description_

    Returns:
        dict: output chunk totally cleaned and ready
    """
    chunks_dsp2_list_1 = chunks_dsp2_list[beginning:end]
    def ajouter_espace_article(texte): return re.sub(r'(Article\s+\d+)\s*([^\d\s])', r'\1  \2', texte)
    chunks_dsp2_list_2 = [ajouter_espace_article(i) for i in chunks_dsp2_list_1]
    chunks_dsp2_dict = {i[:11].strip(): i[11:].strip() for i in chunks_dsp2_list_2}
    return chunks_dsp2_dict

def chunker_1_all(beginning: int, end:int, input_data_to_chunk: str) -> dict:
    """All steps optimal article chunker. Tested on AML5, CRR and DSP2.

    Args:
        input_data_to_chunk (str): texte entrée a chunker apres conversion de pdf

    Returns:
        dict: of chunks
    """
    article_splitter = RecursiveCharacterTextSplitter(separators= ["Article"],chunk_size= 300, chunk_overlap=0)
    chunks= article_splitter.split_text(input_data_to_chunk)
    chunks = chunks[beginning:end]
    def ajouter_espace_article(texte): return re.sub(r'(Article\s+\d+)\s*([^\d\s])', r'\1  \2', texte)
    chunks=[ajouter_espace_article(i) for i in chunks]
    chunks_dic = {item[:11].strip(): item[10:].lstrip() for item in chunks}
    return chunks_dic

# Chunker 2 : approche qui définit un chunk document pour chaque article

def chunker_2_doc(chunks_UE_dict: dict, Directive_source:str):
    """
    ## Option Facultative : dict -> list of docs + metadata
    
    Args:
        chunks_UE_dict (dict): Dictionnaire id sont articles et les clés contenus. 
        Directive_source (str): Nom ou référence de la directive UE. 

    Returns:
        dict: Document(id='1', metadata={'Directive_source': 'DPS2', 'N°article ': 'pre'}, page_content='mier Objet)
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

# Chunker 3 : un article par doc puis chaque doc chunké 


# Chunker 4 : un chunk document pour chaque article

def chunker_4(beginning: int, end:int, input_data_to_chunk: str) -> list:
    """Chunker by "CHAPITRE", "SECTION", "Article".
    ## Incomplete + non reliable
    "SECTION" peut etre espacé...
    Args:
        input_data_to_chunk: texte entrée a chunker apres conversion de pdf

    Returns:
        list: of chunks
    """
    article_splitter = RecursiveCharacterTextSplitter(
    separators= ["CHAPITRE", "SECTION", "Article"],
    chunk_size= 100,
    chunk_overlap=0)
    chunks= article_splitter.split_text(input_data_to_chunk)
    chunks = chunks[beginning:end]
    def ajouter_espace_article(texte): return re.sub(r'(Article\s+\d+)\s*([^\d\s])', r'\1  \2', texte)
    chunks=[ajouter_espace_article(i) for i in chunks]
    return chunks

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

