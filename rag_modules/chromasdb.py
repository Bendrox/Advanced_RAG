from langchain.vectorstores import Chroma

def input_data_chromasdb(namedb, chunks,nom_source, embedding_model, chemin):
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
    namedb = Chroma.from_texts( 
        texts=chunks,
        metadatas= [{"source": nom_source} for _ in chunks],
        persist_directory=chemin,
        embedding=embedding_model)

def qa_vectordb(namedb, question, k_numer ,source_filter):
    """
    Effectue une recherche de similarité dans une base vectorielle Chroma, 
    filtrée par source, et retourne les documents les plus proches de la question.

    Args:
        namedb (Chroma): Instance d'une base vectorielle Chroma initialisée.
        question (str): Question posée à laquelle on cherche des passages similaires.
        k_numer (int): Nombre de documents similaires à retourner.
        source_filter (str): Valeur de filtre sur la métadonnée "source" pour restreindre la recherche.

    Returns:
        List[Document]: Liste des documents les plus similaires trouvés.
    """
    docs = namedb.similarity_search(question,k_numer, filter={"source":source_filter})
    
        

