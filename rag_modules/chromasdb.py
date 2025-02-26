from langchain.vectorstores import Chroma

def input_data_chromasdb(chunks, embedding_model, chemin,nom_source):
    vectordb = Chroma.from_texts( 
        texts=chunks,
        metadatas= [{"source": nom_source} for _ in chunks],
        persist_directory=chemin,
        embedding=embedding_model)

