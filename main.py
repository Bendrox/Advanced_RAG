# Importing data pipelines
from data_pipelines.url_extractor import url_to_local_pdf, firecrawl_extractor_mrkd
from data_pipelines.token_counter import count_tokens
from data_pipelines.txt_saver_loader import load_txt
from data_pipelines.data_cleaning import (supr_avant_directive_mrk, supr_apres_directive_mrk, 
                                          nettoyer_markdown, weird_carac_remove, 
                                          supr_avant_reglement_mrk, supr_apres_reglement_mrk)

from data_pipelines.txt_saver_loader import load_txt, save_txt

## importing LLM
from llm_tools.chunker import chunker_optimal
from llm_tools.lcqa import get_eu_data_4p, get_eu_data_3p
from models.llm_models import llm_4o, llm_4omini, llm_stream_response

# Global import 
import os 

###### Step 1: inject URL for Firecrawl
print("Début de l'étape 1: injection des liens")
url_aml5="http://publications.europa.eu/resource/celex/32015L0849"
url_crr="http://publications.europa.eu/resource/celex/32013R0575"
print("Etape 1 terminée")

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

###### Step 3: calcul nombre de token de l'extraction brute 
print("Début de l'étape 3: calcul du nombre de token de l'extraction brute")
print(f"Le nombre de count_tokens du texte brute est de : {count_tokens(scrape_result)}")
print("Etape 3 terminée")

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

###### Step 5: Option 1: LCQA - Long context Question answering 
print("Début de l'étape 5: Long context Question answering")

# load test data
art_1_old = load_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_input/art_l561_2_old.txt")
art_1_new = load_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_input/art_l561_2_new.txt")

# Inject data for QA 
lcqa_3p_res=get_eu_data_3p(llm_4o,scrape_result_5,art_1_old, art_1_new)
lcqa_4p_res=get_eu_data_4p(llm_4o,scrape_result_5,art_1_old, art_1_new)

# save llm response 
save_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_llm_output/llm_rep_3p.txt",lcqa_3p_res)
save_txt("/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_llm_output/llm_rep_4p.txt",lcqa_4p_res)

print("Fin de l'étape 5: Long context Question answering")

###### Step 6: RAG 
print("Début de l'étape 6: RAG building")

# chunking 
print("Début de l'étape 6.1: chunking")
chunks = chunker_optimal(scrape_result_5)
print("Fin de l'étape 6.1: chunking")

###### Step 7:
