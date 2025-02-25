from firecrawl import FirecrawlApp
import os 

app = FirecrawlApp(api_key=os.getenv('api_key_firecraw_2'))

def firecrawl_extractor(input:str):
    scrape_result = app.scrape_url(
        input,
        params={
            'formats': ['markdown', 'html'],
            'location': {
                'country': 'FR'
            }
        }
    )
    return scrape_result

