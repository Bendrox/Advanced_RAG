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
        
def pipe_1_url_to_pdf(url, save_path):
    """Optimized pipeline Transform local URL eurlex to a local file PDF

    Args:
        url (_type_): url of eurlex , exemple: http://publications.europa.eu/resource/celex/32013R0575
        save_path (_type_): give your local path
    """
    response = requests.get(url, 
                            headers={"Accept": "application/pdf"})
    # tres important pour ne pas renvoyer rdf ou autre format...
    with open(save_path, "wb") as f:
        f.write(response.content)
        
        
#### Unused old functions : 
    
def url_to_local_pdf(eurlex_url, save_path):
    """pipeline Transform local URL eurlex to a local file PDF

    Args:
        eurlex_url (_type_): url of eurlex , exemple: http://publications.europa.eu/resource/celex/32013R0575
        save_path (_type_): give your local path
    """
    response = requests.get(eurlex_url)
    with open(save_path, "wb") as f:
        f.write(response.content)