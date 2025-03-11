from models.llm_models import llm_4omini
from pprint import pprint

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate

def qa_vector_chromasdb(chromasdb,question, k_numer ,source_filter):
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
    docs = chromasdb.similarity_search(question,k_numer, filter={"source":source_filter})
    return docs

def qa_vector_chromasdb_simil_score(vector_chromasdb, question, k_numer ,source_filter):
    """ 
    Similarity search with Chroma with distance.
    Lower score represents more similarity.
    """
    results = vector_chromasdb.similarity_search_with_score(query=question,
                                                            k=k_numer,
                                                            filter={"source":source_filter})
    return results


def qa_vector_chromasdb_simil_score_normal(vector_chromasdb, question:str, k_numer :int,source_filter:str):
    """ 
    1 : Indique une correspondance parfaite.
    0 : Une absence de similarité.
    """
    results = vector_chromasdb.similarity_search_with_relevance_scores(query=question,
                                                            k=k_numer,
                                                            filter={"source":source_filter})
    #return pprint(results)
    for doc, score in results:
        print(f"\n * SIM={score:.3f} ,{vector_chromasdb._collection_name} ,metadata: {doc.metadata} : {doc.page_content} ")
        
def qa_llm_vectordb_chroma(vectordb_name,question,k):
    """
    Exécute une requête question/réponse en utilisant :
    - une base vectorielle (type Chroma) pour retrouver les documents pertinents,
    - un modèle de langage pour générer une réponse concise à partir de ces documents.

    Args:
        vectordb_name (Chroma): Base vectorielle contenant les documents à interroger.
        question (str): La question posée par l'utilisateur.
        k (int): Le nombre de documents les plus similaires à récupérer depuis la base.

    Returns:
        dict: Résultat retourné par la chaîne LLM avec la réponse générée et éventuellement les documents sources.
    """
    prompt = (
    "Utilise le contexte donné pour répondre à la question. "
    "Si tu ne connais pas la réponse, dis le. "
    "Utilise trois phrases maximum et sois concis."
    "Contexte : {context}"
    )
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", prompt),
        ("human", "{input}"),
    ]
)
    question_answer_chain = create_stuff_documents_chain(llm_4omini, prompt)
    retriever = vectordb_name.as_retriever(search_kwargs={"k": k})
    chain = create_retrieval_chain(retriever, question_answer_chain)
    resultat = chain.invoke({"input": question})
    return resultat
