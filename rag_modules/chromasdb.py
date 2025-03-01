from langchain.vectorstores import Chroma

def input_data_chromasdb(chunks,nom_source, embedding_model, chemin):
    """
    Crée une base de données vectorielle Chroma à partir de textes segmentés, 
    en les encodant avec un modèle d'embedding, et en les stockant avec persistance.

    Args:
        namedb (str): Nom de la base de données vectorielle (pas utilisé dans cette fonction, mais peut être utile pour gestion externe).
        chunks (List[str]): Liste de morceaux de texte (documents découpés) à indexer.
        nom_source (str): Nom de la source associée à chaque chunk (utilisé pour les métadonnées).
        embedding_model (Embeddings): Modèle d'embedding compatible LangChain pour encoder les textes.
        chemin (str): Chemin du dossier où persister la base Chroma (persist_directory).

    Returns:
        Chroma: Instance de la base de données Chroma créée avec les textes indexés.
    """
    chroma_db = Chroma.from_texts( 
        texts=chunks,
        metadatas= [{"source": nom_source} for _ in chunks],
        persist_directory=chemin,
        embedding=embedding_model)
    return chroma_db

        

