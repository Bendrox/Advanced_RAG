# Global import 
import os 

# Importing data pipelines
from data_pipelines.optim_data_pip import pipe_1_url_to_pdf, pipe_2_pdf_txt, pipe_3_nettoyer_texte
from data_pipelines.token_counter import str_count_tokens
from data_pipelines.saver_loader import load_txt, save_txt, save_dict_json

## importing for LLM
from llm_tools.chunker import (chunker_1_step_1,chunker_1_step_2 
                               ,chunker_1_all,chunker_2_doc,
                               chunker_3_all, chunker_4, list_chunk_stat_token)
from llm_tools.lcqa import get_eu_data_4p, get_eu_data_3p
from models.llm_models import llm_4o, llm_4omini, llm_stream_response 

#importing for RAG
from models.embedding_models import emb_3_large, funct_embedding_openai_3l
from rag_modules.chromasdb import (source_exists_in_chroma, load_existing_chromasdb, 
        input_chunks_chromasdb, input_chunks_chromasdb_v2, source_exists_in_chroma_v3)
from rag_modules.qa import (qa_llm_vectordb_chroma, qa_vector_chromasdb, 
                            qa_vector_chromasdb_simil_score, qa_vector_chromasdb_simil_score_normal)


# Langchain 
from langchain_chroma import Chroma


###### Step 1: inject data
print("---------------------------------------")
print("Début de l'étape 1: injection des données (local paths , URLs, Options utilisateur...)")

### Variables statiques:
url_aml_5_pdf="https://eur-lex.europa.eu/legal-content/FR/TXT/PDF/?uri=CELEX:32015L0849"
url_crr_pdf="https://eur-lex.europa.eu/legal-content/FR/TXT/PDF/?uri=CELEX:32013R0575"
url_dsp2_pdf="https://eur-lex.europa.eu/legal-content/FR/TXT/PDF/?uri=CELEX:32015L2366"

chroma_db_path = "/Users/oussa/Desktop/Github_perso/Advanced_RAG/vector_store/chromasdb"

### Choix utilisateur:
# 1) Question RAG: 
# Pour AML
question_test_1="Est est l'objectif de la directive ?"
question_test_2 = "Dans quels cas la directive AML 5 impose-t-elle une mesure de vigilance renforcée (« enhanced due diligence ») ?"
question= question_test_2 #choix question ici 


# 2) Long context question ansering 
lcqa="Non"  # "Oui" "Non"

# 3) Contenu UE: réglement / directive: 
url_ue= url_aml_5_pdf # ici choix 
source_name="aml_5" # "aml_5" "dsp2"

# 4) Chunk strategies:
chunk_stratégie=1 # 1 chaque article dans un chunk
                  # 2 chaque article dans un chunk (format document avec metadonnées)
                  # 3 Double chunk : 1 article dans 1 chunk (doc + meta) rechunké
                  # Not use 4 chaque article ds doc + structure Chapitre sec...

nbr_art=70 # nombre d'articles pour chunck

# 5) embedding model :
embedding_model= emb_3_large
emb_model_name = embedding_model.model_dump()["model"]

print("Etape 1 terminée")
print("---------------------------------------")

###### Step 2: Eurlex URL to PDF
print("Début de l'étape 2: récupération des données depuis Eurlex , sauvegarde puis chargement depuis fichier local")

if not os.path.exists(f"/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_scrapped/{source_name}.pdf"): 
    print("Etape 2: Fichier n'existe pas , récupération en cours")

    pipe_1_url_to_pdf(url_ue,f"/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_scrapped/{source_name}.pdf")
    print("Etape 2: Fichier sauvegardé localement avec succès !")
    scrape_result=pipe_2_pdf_txt(f"/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_scrapped/{source_name}.pdf")

else:
    print("Etape 2: Fichier existant dans répertoire local")
    scrape_result=pipe_2_pdf_txt(f"/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_scrapped/{source_name}.pdf")
    
print("Etape 2 terminée: données européennes en local.")
print("---------------------------------------")

###### Step 3: calcul nombre de token de l'extraction brute 
print("Début de l'étape 3: calcul du nombre de token de l'extraction brute")
print(f"Le nombre de count_tokens du texte brute est de : {str_count_tokens(scrape_result)}")
print("Etape 3 terminée")
print("---------------------------------------")

####### Step 4: Netoyage du text brut 
print("Début de l'étape 4: Netoyage du text brut ")
scrape_result_clean = pipe_3_nettoyer_texte(scrape_result)

print("Succès de l'étape 4: Netoyage du text brut ")
print(f"Nombre de token après nettoyage du text: {str_count_tokens(scrape_result_clean)}")
diff_nettoyage= str_count_tokens(scrape_result) - str_count_tokens(scrape_result_clean)
print(f"Nombre de token supprimés grace au nettoyage : {diff_nettoyage}  ")
print("---------------------------------------")

###### Step 5: Option 1: LCQA - Long context Question answering 
print("Début de l'étape 5: Long context Question answering")

# load test data
art_1_old = load_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_input/art_l561_2_old.txt")
art_1_new = load_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_input/art_l561_2_new.txt")

# Inject data for QA 

if lcqa == "Oui": 
    lcqa_3p_res=get_eu_data_3p(llm_4o,scrape_result_clean, art_1_old, art_1_new)
    lcqa_4p_res=get_eu_data_4p(llm_4o,scrape_result_clean, art_1_old, art_1_new)
    # save llm response 
    save_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_llm_output/llm_rep_3p.txt",lcqa_3p_res)
    save_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_llm_output/llm_rep_4p.txt",lcqa_4p_res)

else: print("Choix de l'utilisateur de ne pas faire du Long context Question answering.")

print("Fin de l'étape 5: Long context Question answering")
print("---------------------------------------")

###### Step 6: RAG 
print("Début de l'étape 6: RAG . Décomposition du RAG en plusieurs étapes:")
print("---------------------------------------")

# étape 6.1: chunking 
print("Début de l'étape 6.1: Chunking\n")

# Modular 3 cases
if chunk_stratégie == 1:
    chunks=chunker_1_all(1,nbr_art,scrape_result_clean)
elif chunk_stratégie == 2:
    chunks=chunker_1_all(1,nbr_art,scrape_result_clean)
    chunks=chunker_2_doc(chunks, source_name)
else:
    chunks=chunker_1_all(1,nbr_art,scrape_result_clean)
    chunks=chunker_2_doc(chunks, source_name)
    chunks=chunker_3_all(scrape_result_clean)
    
print("Strategie de chunking choisie: {chunk_stratégie}")
print("Fin de l'étape 6.1: Chunking")
print("---------------------------------------")

# étape 6.2: list to dict 
print("Début de l'étape 6.2: Save chunks")
save_dict_json(f"/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_chunks/chunks_{source_name}_strat_{chunk_stratégie}.json", chunks)
print("Fin de l'étape 6.2: Save chunks")
print("---------------------------------------")

# étape 6.3: Embedding + stockage chromasdb
# Essayer Milvus , FAISS, picorn ?

print("Début de l'étape 6.3: Chunks embedding to vector database")
### Resultat recherché: 
# 1 seul chromasDB
# 3 stratégies de chunks en collection_name
# nom de la directive en metadonnées paramètre source 

if source_exists_in_chroma_v3(chroma_db_path, source_name ,embedding_model,emb_model_name,1):
    print('Données existentes dans ChromasDB') 
    global chromasdb
    chromasdb = load_existing_chromasdb(chroma_db_path, embedding_model)
    
    
else:
    print('Données non existentes dans ChromasDB, chargement en cours dans la base vectorielle...') 
    if chunk_stratégie == 1: # dict input
        chromasdb = input_chunks_chromasdb_v2(chunks, 
                                            source_name, 
                                            embedding_model, 
                                            emb_model_name,
        "/Users/oussa/Desktop/Github_perso/Advanced_RAG/vector_store/chromasdb",
                                            1)
        print("Nombre de vecteurs de stratégie 1:", chromasdb._collection.count()) 
        chromasdb.similarity_search_with_relevance_scores("", 5)       

    else: 
        chromasdb.add_documents(chunks)
        
    
print("Fin de l'étape 6.3: Chunks embedding to vector database, ")
print("---------------------------------------")

# étape 6.4: QA retreival test:
print("Début de l'étape 6.4: QA article retreival similarity score")

print(f"\nQuestion de l'utilisateur: {question}")
print(f"\nRetreival result:\n")
qa_vector_chromasdb_simil_score_normal(chromasdb,question,4,source_name)
# intégrer pprint
print("\nFin de l'étape 6.4: QA article retreival similarity score")
print("---------------------------------------")

# étape 6.5: QA retreival + llm test:
print("Début de l'étape 6.5: QA article retreival + llm \n")

res_rag_1 = qa_llm_vectordb_chroma(chromasdb,question,3)
print(res_rag_1['answer'])
res_rag_1_str = str(res_rag_1['answer'])
save_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_llm_output/rag1.txt",res_rag_1_str)

print("\nFin de l'étape 6.5: QA article retreival + llm ")
print("---------------------------------------")

# Etape 6.6 : 

# Etape 6.7: Reranking :

# - Azure AI Search 
# - llm rerank 

# option 1: llm


# option 2: 



###### Step 7:
