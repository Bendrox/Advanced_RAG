from data_pipelines.url_extractor import url_to_local_pdf, firecrawl_extractor_mrkd


url_aml_5="http://publications.europa.eu/resource/celex/32015L0849"
url_crr="http://publications.europa.eu/resource/celex/32013R0575"

url_to_local_pdf("https://eur-lex.europa.eu/legal-content/FR/TXT/PDF/?uri=CELEX:32018L0843", 
                "/Users/oussa/Desktop/Github_perso/Advanced_RAG/data_input/AML5.pdf")



# Step 1: inject URL for Firecrawl
url_aml_5="http://publications.europa.eu/resource/celex/32015L0849"
url_crr="http://publications.europa.eu/resource/celex/32013R0575"

# step 2: scraping data with firecrawl  
scrape_result = firecrawl_extractor_mrkd(url_aml_5)

# step 3:
scrape_result['Markdown']

# step 4:

# step 5:

# step 6:

# step 7:
