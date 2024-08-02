import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup
from lxml import html
from datetime import datetime
from PyPDF2 import PdfFileReader
from io import BytesIO
from urllib.parse import quote
from dotenv import load_dotenv
import os

# 環境変数を読み込む
load_dotenv()

entries = []

# 環境変数からプロキシサーバリストを取得
proxies = [
	os.getenv("PROXY1"),
    os.getenv("PROXY2")
]
proxy_index = 0

# プロキシを交互に選択する関数
def get_next_proxy():
    global proxy_index
    proxy = proxies[proxy_index]
    proxy_index = (proxy_index + 1) % len(proxies)
    return f"http://{proxy}"

#03 convert lxml data from Arxiv Web Site
async def fetch_arxiv(session, url):
    proxy = get_next_proxy()
    async with session.get(url, proxy=proxy) as res:
        content = await res.text()
        soup = BeautifulSoup(content, "lxml")
        soup_str = str(soup)
        soup_bytes = bytes(soup_str, encoding="utf8")
        lxml_data = html.fromstring(soup_bytes)
        
        return lxml_data

#04 download the PDF and count the pages
async def fetch_pdf(session, url):
    pdf_url = url.replace("abs", "pdf")
    
    try:
        proxy = get_next_proxy()
        async with session.get(pdf_url, proxy=proxy) as res:
            pdf_data = await res.read()
            return res.status, pdf_data
    except:
        return 404, None

#05 scrap Conference and num of citation 
async def fetch_semantic(session, url):
    #Encode URL
    encoded_url = quote(f"URL:{url}")

    # Base URL
    base_url = "https://api.semanticscholar.org/graph/v1/paper/"

    # Query params
    fields = "citationCount,influentialCitationCount,venue,publicationVenue,publicationTypes,journal"
    
    # Full URL
    full_url = f"{base_url}{encoded_url}?fields={fields}"

    try:
        async with session.get(full_url) as response:
            res = await response.text()
            res_json = json.loads(res)
            
            # Extract conference, citation count
            venue = res_json.get("venue")
            citation_count = res_json.get("citationCount")
            
            return venue, citation_count
    except:
        return None, None

#02 scraping from several method
async def fetch_data(session, queryDetails):
    url = queryDetails["url"]
    
    # In case of direct link to PDF, change the link
    if "https://arxiv.org/pdf/" in url:
        url = url.replace("pdf", "abs")
    
    arxiv_data = await fetch_arxiv(session, url)
    pdf_status, pdf_data = await fetch_pdf(session, url)
    venue, citation_count = await fetch_semantic(session, url)
    
    return queryDetails, arxiv_data, pdf_status, pdf_data, venue, citation_count

#01 load from query array
async def load_site_contents(queryData):
    async with aiohttp.ClientSession() as session:
        try:
            # Call scraping functions
            tasks = [fetch_data(session, queryDetails) for queryDetails in queryData]
            results = await asyncio.gather(*tasks)
            
            # Add scholar info from scraped data
            for queryDetails, arxiv_data, pdf_status, pdf_data, venue, citation_count in results:
                # Title
                title = arxiv_data.xpath("//meta[@property='og:title']/@content")[0]
                
                # Author
                author = arxiv_data.xpath("//div[@class='authors']/a/text()")
                authors = ", ".join(author)
                
                # Conference 
                if arxiv_data.xpath("//td[@class='tablecell comments mathjax']/text()"):
                    conf_text = arxiv_data.xpath("//td[@class='tablecell comments mathjax']/text()")[0]
                    
                    # 査読元を学会とする
                    search_terms = ['Accepted by ', 'Accepted for ', 'Published as', 'accepted', 'publish']
                    
                    # 小文字に変換してから検索
                    conf_text_lower = conf_text.lower()
                    conference = None
                    
                    for term in search_terms:
                        index = conf_text_lower.find(term.lower())
                        if index != -1:
                            conference = conf_text[index + len(term):]
                            break  
                        
                    # APIにより学会見つかった場合変更
                    if venue:   
                        conference = venue
                else:
                    conference = venue or None
                
                # Pages
                if pdf_status == 200 and pdf_data:
                    pdf_file = BytesIO(pdf_data)
                    pdf_reader = PdfFileReader(pdf_file)
                    pages = pdf_reader.getNumPages()      
                else:
                    pages = None
                
                # Date
                dateline = arxiv_data.xpath("//div[@class='dateline']/text()")[0].strip()
                date_part = dateline.strip('[]').replace('Submitted on ', '')
                clean_date_part = date_part.split(' ')[0:3]
                clean_date_str = ' '.join(clean_date_part)
                date_obj = datetime.strptime(clean_date_str, '%d %b %Y')
                date = date_obj.strftime('%y%m%d')
                
                # Abstract
                abstract = arxiv_data.xpath("//meta[@property='og:description']/@content")[0]
                
                # Cite num
                cite_num = citation_count
                
                # Submitted
                submitted = bool(arxiv_data.xpath("//td[@class='tablecell comments mathjax']/text()"))
                
                # Add entry
                add_entry(queryDetails["url"], title, authors, conference, pages, date, abstract, cite_num, submitted, queryDetails["relevant_no"])
        except Exception as e:
            print(f"Error occurred: {e}")

#06 func to add to entry 
def add_entry(url, title, author, conference, pages, date, abstract, cite_num, submitted, relevant_no):
    new_entry = {
        "url": url,
        "title": title,
        "author": author,
        "conference": conference,
        "pages": pages,
        "date": date,
        "abstract": abstract,
        "cite_num": cite_num,
        "submitted": submitted,
        "relevant_no": relevant_no,
    }
    entries.append(new_entry)

# MAIN
def load_arxiv_contents(queryData):
    asyncio.run(load_site_contents(queryData))
    return entries
