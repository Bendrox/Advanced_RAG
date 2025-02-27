from data_pipelines.url_extractor import url_to_local_pdf, firecrawl_extractor_mrkd
from data_pipelines.token_counter import count_tokens


# Step 1: inject URL for Firecrawl
print("Début de l'étape 1")

url_aml_5="http://publications.europa.eu/resource/celex/32015L0849"
url_crr="http://publications.europa.eu/resource/celex/32013R0575"

print("Etape 1 terminée")

# step 2: scraping data with firecrawl
print("Début de l'étape 2: récupérer les données avec firecrawl ")

scrape_result = firecrawl_extractor_mrkd(url_aml_5)

print("Etape 2 terminée")

# step 3: calcul nombre de token de l'extraction brute 
print("Début de l'étape 3: calcul nombre de token de l'extraction brute")

print(f"Le nombre de count_tokens du texte brute est de : {count_tokens(scrape_result)}")

print("Etape 3 terminée")

# step 4: Netoyage du text brut 
print("Début de l'étape 4: Netoyage du text brut")


# step 5:

# step 6:

# step 7:
