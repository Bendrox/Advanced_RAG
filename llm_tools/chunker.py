from langchain_text_splitters import RecursiveCharacterTextSplitter

# attention RecursiveCharacterTextSplitter	Si le « morceau » résultant dépasse chunk_size, 
# il redescend au séparateur suivant (plus petit).


def chunker_optimal(input_data_to_chunk):
    """Optimal chunker for AML5 + CRR

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

def chunks_list_dict():
chunks_aml5_dic = {item[:10]: item[10:].lstrip() for item in chunks_aml5}
