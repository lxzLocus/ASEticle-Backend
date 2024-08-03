import aiohttp
import requests
import sys
import os
from bs4 import BeautifulSoup
from lxml import html
from datetime import datetime
from urllib.parse import quote

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))) #追加
from config.localization import Localization

entries = []


ACM_URL = "https://acm.org/"

class WebScraper:

    def __init__(self, url):
        self.url = url
        self.page_content = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def fetch_page(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            self.page_content = response.content
        except requests.exceptions.HTTPError as err:
            print(Localization.get('app.module.acm.fetch.http_error') + {err})
        except Exception as e:
            print(Localization.get('app.module.acm.fetch.error') + {e})

    def extract_metadata(self):
        if not self.page_content:
            print(Localization.get('app.module.acm.extract.fetch_error'))
            return html.Element("html")

        # Extract using XPATH
        extractContent = html.fromstring(self.page_content)
        if extractContent is None:
            print(Localization.get('app.module.acm.extract.not_found'))
            return html.Element("html")

        return extractContent

class SemanticApi:
    @classmethod
    async def fetch_semantic_api(cls, url):
        async with aiohttp.ClientSession() as session:
            base_url = "https://api.semanticscholar.org/graph/v1/paper/"
            encoded_url = quote(f"URL:{url}")
            fields = "citationCount,venue"
            
            async with session.get(
                f"{base_url}{encoded_url}?fields={fields}"
            ) as response:
                result = await response.json()

            if result:
                # Ensure venue and citationCount are fetched correctly
                venue = result.get("venue", None)
                citation_count = result.get("citationCount", None)
                author_list = result.get("authors")
                if author_list:
                    author_names = [author["name"] for author in author_list]
                    authors=", ".join(author_names)
                else:
                    authors = None
                if result.get("abstract") and result.get("abstract") != "[]":
                    api_abs = result.get("abstract")
                else:
                    api_abs = None
                return venue, citation_count, authors, api_abs
            else:
                return None, None, None, None

async def execute(param):
    entries = []

    for item in param:
        
        #pdfの場合の処理
        if "/pdf/" in item["url"]:
            item["url"] = item["url"].replace("/pdf/", "/abs/")
        
        url = item["url"]
        relevant_no = item["relevant_no"]
        cite_num = item["cite_num"]
        scraper = WebScraper(url)
        scraper.fetch_page()

        metadata = scraper.extract_metadata() # type: html.HtmlElement

        if len(metadata) > 0:
            # Retrieving contents from metadata
            title = metadata.xpath("//meta[@property='og:title']/@content")[0]
            authors = ", ".join(metadata.xpath("//div[@class='authors']/a/text()"))
                
            
            dateline = metadata.xpath("//*[@id='skip-to-main-content']/main/article/header/div/div[5]/span[2]/text()")[0].strip()
            date_obj = datetime.strptime(dateline, '%d %B %Y')
            date = date_obj.strftime('%Y%m%d')
            
            try:
                start_page = int(metadata.xpath('//span[@property="pageStart"]/text()')[0])
                end_page = int(metadata.xpath('//span[@property="pageEnd"]/text()')[0])
                pages = end_page - start_page + 1
            except:
                pages = None
            
            venue, cite_num, authors, api_abs = await SemanticApi.fetch_semantic_api(url)
            
            if api_abs is None:
                abstract = metadata.xpath("//*[@id='abstract']/div/text()")[0]
            else:
                abstract = api_abs
                
            submitted = True # ACMの場合は常にTrue
            
            new_entry = {
                "url": url,
                "title": title,
                "author": authors,
                "conference": venue,
                "pages": pages,
                "date": date,
                "abstract": abstract,
                "cite_num": cite_num,
                "submitted": submitted,
                "relevant_no": relevant_no,
            }
            entries.append(new_entry)

    return entries
