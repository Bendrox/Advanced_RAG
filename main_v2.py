# Importing data pipelines
from data_pipelines.url_extractor import pipe_1_url_to_pdf
from data_pipelines.token_counter import count_tokens
from data_pipelines.txt_saver_loader import load_txt
from data_pipelines.data_cleaning import (supr_avant_directive_mrk, supr_apres_directive_mrk, 
                                          nettoyer_markdown, weird_carac_remove, 
                                          supr_avant_reglement_mrk, supr_apres_reglement_mrk)

from data_pipelines.txt_saver_loader import load_txt, save_txt, save_dict_json

## importing LLM
from llm_tools.chunker import chunker_optimal, chunks_list_to_dict
from llm_tools.lcqa import get_eu_data_4p, get_eu_data_3p
from models.llm_models import llm_4o, llm_4omini, llm_stream_response 

#importing RAG
from models.embedding_models import emb_3_large, funct_embedding_openai_3l
from rag_modules.chromasdb import input_data_chromasdb, source_exists_in_chroma, load_existing_chromasdb
from rag_modules.qa import  qa_llm_vectordb_chroma, qa_vector_chromasdb

# Global import 
import os 

# Langchain 
from langchain_chroma import Chroma


###### Step 1: inject data
print("---------------------------------------")
print("Début de l'étape 1: injection des données")


chroma_db_path = "/Users/oussa/Desktop/Github_perso/Advanced_RAG/vector_store/chromasdb"
source_name = "aml_5"
url_aml5="http://publications.europa.eu/resource/celex/32015L0849"
url_crr="http://publications.europa.eu/resource/celex/32013R0575"


print("Etape 1 terminée")
print("---------------------------------------")

###### Step 2: scraping data with firecrawl
print("Début de l'étape 2: récupération des données avec firecrawl ou chargement depuis fichier local")

if not os.path.exists("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_scrapped/aml5.txt"): 
    print("Etape 2: Fichier n'existe pas , appel a Firecrawl pour récupération")
    scrape_result = firecrawl_extractor_mrkd(url_aml5)
    save_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_scrapped/aml5.txt",scrape_result)
else:
    print("Etape 2: fichier existe récupération a partir du fichier local")
    scrape_result= load_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_scrapped/aml5.txt")
    
print("Etape 2 terminée")
print("---------------------------------------")

###### Step 3: calcul nombre de token de l'extraction brute 
print("Début de l'étape 3: calcul du nombre de token de l'extraction brute")
print(f"Le nombre de count_tokens du texte brute est de : {count_tokens(scrape_result)}")
print("Etape 3 terminée")
print("---------------------------------------")

####### Step 4: Netoyage du text brut 
print("Début de l'étape 4: Netoyage du text brut (en 5 étapes)")
scrape_result_1= supr_avant_directive_mrk(scrape_result)
scrape_result_2= supr_apres_directive_mrk(scrape_result_1)
scrape_result_3= nettoyer_markdown(scrape_result_2)
scrape_result_4= nettoyer_markdown(scrape_result_3)
scrape_result_5= weird_carac_remove(scrape_result_4)
print("Succès de l'étape 4: Netoyage du text brut (en 5 étapes)")
print(f"Nombre de token après nettoyage du text: {count_tokens(scrape_result_5)}")
diff_nettoyage= count_tokens(scrape_result) - count_tokens(scrape_result_5)
print(f"Nombre de token supprimés grace au nettoyage : {diff_nettoyage}  ")
print("---------------------------------------")

###### Step 5: Option 1: LCQA - Long context Question answering 
print("Début de l'étape 5: Long context Question answering")

# load test data
art_1_old = load_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_input/art_l561_2_old.txt")
art_1_new = load_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_input/art_l561_2_new.txt")

# Inject data for QA 
lcqa_3p_res=get_eu_data_3p(llm_4o,scrape_result_5, art_1_old, art_1_new)
lcqa_4p_res=get_eu_data_4p(llm_4o,scrape_result_5, art_1_old, art_1_new)

# save llm response 
save_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_llm_output/llm_rep_3p.txt",lcqa_3p_res)
save_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_llm_output/llm_rep_4p.txt",lcqa_4p_res)

print("Fin de l'étape 5: Long context Question answering")
print("---------------------------------------")

###### Step 6: RAG 
print("Début de l'étape 6: RAG building")

# chunking 
print("Début de l'étape 6.1: chunking")
chunks = chunker_optimal(scrape_result_5)
print("Fin de l'étape 6.1: chunking")
print("---------------------------------------")

# list to dict 
print("Début de l'étape 6.2: list to dict")
chunks_dic=chunks_list_to_dict(chunks)
save_dict_json("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_output_chunks/chunks.json", chunks_dic)
print("Fin de l'étape 6.2: list to dict")
print("---------------------------------------")

# output:
# {'Article 69': 'Les États membres sont destinataires de la présente directive...'}

# embedding + stockage chromasdb
# funct_embedding_openai_3l()
print("Début de l'étape 6.3: chunks to vector database")

if source_exists_in_chroma(chroma_db_path, source_name ,emb_3_large):
    print('Données existentes dans ChromasDB') 
    global vector_chromasdb
    vector_chromasdb = load_existing_chromasdb(chroma_db_path, emb_3_large)

else:
    print('Données non existentes dans ChromasDB, chargement en cours...') 
    vector_chromasdb = input_data_chromasdb(chunks_dic, source_name, emb_3_large, 
                                                    "/Users/oussa/Desktop/Github_perso/Advanced_RAG/vector_store/chromasdb")
    print(vector_chromasdb._collection.count())        
    
print("Fin de l'étape 6.3: chunks to vector database, ")
print("---------------------------------------")

# QA retreival test:
print("Début de l'étape 6.3: Question test")

question="Est est l'objectif de la directive ?"
res_qa_retreival= qa_vector_chromasdb(vector_chromasdb ,question , 4, "aml_5")
print(res_qa_retreival)
res_qa_retreival_str=str(res_qa_retreival)
save_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_llm_output/qa_response.txt",res_qa_retreival_str)
print("Fin de l'étape 6.3: Question test")
print("---------------------------------------")

# QA retreival + llm test:
print("Début de l'étape 6.4: QA with llm test")
res_rag_1 = qa_llm_vectordb_chroma(vector_chromasdb,question,4)
print(res_rag_1['answer'])
res_rag_1_str = str(res_rag_1['answer'])
save_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_llm_output/rag1.txt",res_rag_1_str)
print("Fin de l'étape 6.4: QA with llm test")
print("---------------------------------------")

###### Step 7:
