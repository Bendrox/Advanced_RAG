from langchain_text_splitters import RecursiveCharacterTextSplitter

from data_pipelines.token_counter import count_tokens
import numpy as np

def chunker_1(input_data_to_chunk: str ) -> list:
    """Optimal chunker by article tested and approved on AML5 + CRR

    Args:
        input_data_to_chunk (_type_): texte entrée a chunker apres conversion de pdf

    Returns:
        list: of chunks
    """
    article_splitter = RecursiveCharacterTextSplitter(
    separators=   ["Article"],
    chunk_size= 100, 
    chunk_overlap=0),
    chunks= article_splitter.split_text(input_data_to_chunk)
    return chunks

def chunker_2(input_data_to_chunk: str) -> list:
    """Chunker by "CHAPITRE", "SECTION", "Article".

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

separators = [
    r"\d+\.\s?[A-Z][a-z]*",  # numéros de paragraphes comme "1.Le ", "2.La ", "3.par" etc.
    "CHAPITRE",
    "SECTION",
    "Article"
]

def chunker_3(input_data_to_chunk: str) -> list:
    article_splitter = RecursiveCharacterTextSplitter(
    separators= separators,
    chunk_size= 100,
    chunk_overlap=0),
    chunks= article_splitter.split_text(input_data_to_chunk)
    return chunks


def chunks_list_to_dict(chunks):
    chunks_dic = {item[:10]: item[10:].lstrip() for item in chunks}
    return chunks_dic

def chunk_stat(your_chunks):
    """Produit des stats sur le nombre de tokens par chunks. 
    Pour but d'améliorer les performances 

    Args:your_chunks
    """
    chunk_lengths = [count_tokens(chunk) for chunk in your_chunks]
    print("Nombre de chunks :", len(your_chunks))
    print("Longueur moyenne des chunks:", np.mean(chunk_lengths))
    print("Longueur max des chunks:", np.max(chunk_lengths))
    print("Longueur min des chunks:", np.min(chunk_lengths))
