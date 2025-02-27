from firecrawl import FirecrawlApp
import os 
import requests

app = FirecrawlApp(api_key=os.getenv('api_key_firecraw_2'))

def firecrawl_extractor_mrkd(url:str):
    """
    Utilise l'API Firecrawl pour extraire le contenu d'une URL donnée.  
    Les données sont récupérées aux formats HTML et Markdown,  
    mais seule la version Markdown est renvoyée.  
      
    Args: url (str): L'URL de la page web à extraire.  
      
    Returns: str Contenu de la page au format Markdown.  
      
    Remarque :  
        La requête est effectuée en spécifiant le pays 'FR' pour  
        adapter le contexte géographique si nécessaire.  
    """
    scrape_result = app.scrape_url(
        url,
        params={
            'formats': ['markdown', 'html'],
            'location': {
                'country': 'FR'
            }
        }
    )
    scrape_result = scrape_result['markdown']
    return scrape_result

    

def url_to_local_pdf(eurlex_url, save_path):
    "Transform local URL to save a local file PDF"
    response = requests.get(eurlex_url)
    with open(save_path, "wb") as f:
        f.write(response.content)