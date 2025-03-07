# Global import 
import os 

# Importing data pipelines
from data_pipelines.optim_data_pip import pipe_1_url_to_pdf, pipe_2_pdf_txt, pipe_3_nettoyer_texte
from data_pipelines.token_counter import count_tokens
from data_pipelines.saver_loader import load_txt, save_txt, save_dict_json

## importing for LLM
from llm_tools.chunker import chunker_1 ,chunker_1_pipe,chunker_2,chunker_3, chunker_3_pipe, chunk_stat_token
from llm_tools.lcqa import get_eu_data_4p, get_eu_data_3p
from models.llm_models import llm_4o, llm_4omini, llm_stream_response 

#importing for RAG
from models.embedding_models import emb_3_large, funct_embedding_openai_3l
from rag_modules.chromasdb import input_data_chromasdb, source_exists_in_chroma, load_existing_chromasdb
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
question_test_1="Est est l'objectif de la directive ?"
question_test_2 = "modifications apportées à l'article visent principalement à élargir et clarifier le champ d'application des groupes concernés par les obligations de transmission d'informations, tout en maintenant les principes fondamentaux de secret professionnel et de protection des données."
question= question_test_2 #choix question ici 

# 2) Long context question ansering 
lcqa="Non"  # "Oui" "Non"

# 3) Contenu UE: réglement / directive: 
url_ue= url_aml_5_pdf # ici choix aml5
source_name = "aml_5" # "aml_5"

# 4) Chunk strategies:
chunk_stratégie=1 # 1 pour articles, 
                  # 2 pour chapitre/ selection/ article
                  # 3 + alinéa
nbr_art=70 # nombre d'articles pour chunck

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
print(f"Le nombre de count_tokens du texte brute est de : {count_tokens(scrape_result)}")
print("Etape 3 terminée")
print("---------------------------------------")

####### Step 4: Netoyage du text brut 
print("Début de l'étape 4: Netoyage du text brut ")
scrape_result_clean = pipe_3_nettoyer_texte(scrape_result)

print("Succès de l'étape 4: Netoyage du text brut ")
print(f"Nombre de token après nettoyage du text: {count_tokens(scrape_result_clean)}")
diff_nettoyage= count_tokens(scrape_result) - count_tokens(scrape_result_clean)
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
    chunks=chunker_1(scrape_result_clean)
elif chunk_stratégie == 2:
    chunks=chunker_2(scrape_result_clean)
else:
    chunks=chunker_3(scrape_result_clean)
    
chunks= chunks[1:nbr_art]
print(f"Statistiques sur les chunks créés:")
print(f"{chunk_stat_token(chunks)}")
print("Fin de l'étape 6.1: Chunking")
print("---------------------------------------")

# étape 6.2: list to dict 
print("Début de l'étape 6.2: List to dict")

if chunk_stratégie == 1:
    chunks_dic=chunker_1_pipe(scrape_result_clean)
elif chunk_stratégie == 2:
    chunks_dic=chunker_2(scrape_result_clean)
else:
    chunks_dic=chunker_3_pipe(scrape_result_clean)
    
    
save_dict_json(f"/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_chunks/chunks_{source_name}_strat_{chunk_stratégie}.json", chunks)
print("Fin de l'étape 6.2: List to dict")
print("---------------------------------------")

# étape 6.3: embedding + stockage chromasdb
# Essayer Milvus , FAISS

print("Début de l'étape 6.3: Chunks to vector database")

if source_exists_in_chroma(chroma_db_path, source_name ,emb_3_large):
    print('Données existentes dans ChromasDB') 
    global vector_chromasdb
    vector_chromasdb = load_existing_chromasdb(chroma_db_path, emb_3_large)

else:
    print('Données non existentes dans ChromasDB, chargement en cours...') 
    vector_chromasdb = input_data_chromasdb(chunks_dic, 
                                            source_name, 
                                            emb_3_large, 
                                                    "/Users/oussa/Desktop/Github_perso/Advanced_RAG/vector_store/chromasdb")
    print(vector_chromasdb._collection.count())        
    
print("Fin de l'étape 6.3: Chunks to vector database, ")
print("---------------------------------------")

# étape 6.4: QA retreival test:
print("Début de l'étape 6.4: Question test article retreival")


res_qa_retreival= qa_vector_chromasdb(vector_chromasdb ,question , 4, "aml_5")

print(f"\nQuestion de l'utilisateur: {question}")
print(f"\nRetreival result:\n")
for res in res_qa_retreival:
    print(f"*** {res.page_content} [{res.metadata}]\n")
    
res_qa_retreival_str=str(res_qa_retreival)
save_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_llm_output/qa_response.txt",
         res_qa_retreival_str)
print("Fin de l'étape 6.4: Question test article retreival")
print("---------------------------------------")

# étape 6.5: QA retreival + llm test:
print("Début de l'étape 6.5: QA article retreival + llm \n")

res_rag_1 = qa_llm_vectordb_chroma(vector_chromasdb,question,3)
print(res_rag_1['answer'])
res_rag_1_str = str(res_rag_1['answer'])
save_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_llm_output/rag1.txt",res_rag_1_str)

print("\nFin de l'étape 6.5: QA article retreival + llm ")
print("---------------------------------------")

# Etape 6.6 : similarity retreival :
print("\nDébut de l'étape 6.6: QA article retreival similarity score ")
qa_vector_chromasdb_simil_score_normal(vector_chromasdb,question,3,source_name)
print("\nFin de l'étape 6.6: QA article retreival similarity score ")

# Etape 6.7: Reranking :

# - Azure AI Search 
# - llm rerank 

# option 1: llm


# option 2: 



###### Step 7:
