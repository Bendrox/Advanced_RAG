#importing
from data_pipelines.url_extractor import url_to_local_pdf, firecrawl_extractor_mrkd
from data_pipelines.token_counter import count_tokens
from data_pipelines.data_cleaning import (supr_avant_directive_mrk, supr_apres_directive_mrk, 
                                          nettoyer_markdown, weird_carac_remove, 
                                          supr_avant_reglement_mrk, supr_apres_reglement_mrk)

from llm_tools.lcqa import get_eu_data_4p, get_eu_data_3p

# Step 1: inject URL for Firecrawl
print("Début de l'étape 1: injection des liens")
url_aml_5="http://publications.europa.eu/resource/celex/32015L0849"
url_crr="http://publications.europa.eu/resource/celex/32013R0575"
print("Etape 1 terminée")

# step 2: scraping data with firecrawl
print("Début de l'étape 2: récupération des données avec firecrawl ")
scrape_result = firecrawl_extractor_mrkd(url_aml_5)
print("Etape 2 terminée")

# step 3: calcul nombre de token de l'extraction brute 
print("Début de l'étape 3: calcul du nombre de token de l'extraction brute")
print(f"Le nombre de count_tokens du texte brute est de : {count_tokens(scrape_result)}")
print("Etape 3 terminée")

# step 4: Netoyage du text brut 
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

# step 5: Option 1: LCQA - Long context Question answering 
lcqa_3p_res= get_eu_data_3p()

lcqa_4p_res=get_eu_data_4p()

# step 6:

# step 7:
