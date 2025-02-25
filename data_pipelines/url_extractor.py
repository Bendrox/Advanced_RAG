from firecrawl import FirecrawlApp
import os 
import requests

app = FirecrawlApp(api_key=os.getenv('api_key_firecraw_2'))

def firecrawl_extractor(url:str):
    "Using firecrawl to extract data from URL. Data retreived in two format (HMTL + Markdown)"
    scrape_result = app.scrape_url(
        url,
        params={
            'formats': ['markdown', 'html'],
            'location': {
                'country': 'FR'
            }
        }
    )
    result_mark= scrape_result['markdown']
    result_html= scrape_result['html']
    

def url_to_pdf(url, save_path):
    "Transform URL to save a local file PDF"
    response = requests.get(url)
    with open(save_path, "wb") as f:
        f.write(response.content)