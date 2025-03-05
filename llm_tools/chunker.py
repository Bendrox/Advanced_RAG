from langchain_text_splitters import RecursiveCharacterTextSplitter

from data_pipelines.token_counter import count_tokens
import numpy as np

def chunker_optimal(input_data_to_chunk):
    """Optimal chunker tested on AML5 + CRR

    Args:
        input_data_to_chunk (_type_): _description_

    Returns:
        list: of chunks
    """
    article_splitter = RecursiveCharacterTextSplitter(
    separators=   ["Article"],
    chunk_size= 100, 
    chunk_overlap=0)
    chunks= article_splitter.split_text(input_data_to_chunk)
    return chunks

def chunks_list_to_dict(chunks):
    chunks_dic = {item[:10]: item[10:].lstrip() for item in chunks}
    return chunks_dic

def chunk_stat(your_chunks):
    """Produit des stats sur le nombre de tokens par chunks. 
    Pour but d'améliorer les performances 

    Args:your_chunks (_type_)
    """
    chunk_lengths = [count_tokens(chunk) for chunk in your_chunks]
    print("Nombre de chunks :", len(your_chunks))
    print("Longueur moyenne des chunks:", np.mean(chunk_lengths))
    print("Longueur max des chunks:", np.max(chunk_lengths))
    print("Longueur min des chunks:", np.min(chunk_lengths))
