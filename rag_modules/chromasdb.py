from langchain.vectorstores import Chroma

def input_data_chromasdb(namedb, chunks,nom_source, embedding_model, chemin):
    namedb = Chroma.from_texts( 
        texts=chunks,
        metadatas= [{"source": nom_source} for _ in chunks],
        persist_directory=chemin,
        embedding=embedding_model)

def qa_chroma(namedb,question, k_numer ,source_filter):
    docs = namedb.similarity_search(question,k_numer, filter={"source":source_filter})
    
        
