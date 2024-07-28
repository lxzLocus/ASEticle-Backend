import aiohttp
import asyncio
import requests
import concurrent.futures
from bs4 import BeautifulSoup
from lxml import html
from datetime import datetime
from PyPDF2 import PdfFileReader
from io import BytesIO
from dotenv import load_dotenv


test_data = [
    {
        "url" : "https://arxiv.org/abs/2403.00448",
        "relevant_no" : 1
    },
    {
        "url" : "https://arxiv.org/abs/2406.05621",
        "relevant_no" :3
    },
    {
        "url" : "https://arxiv.org/abs/2404.05598",
        "relevant_no" : 7
    }
]

entries = []

async def fetch_arxiv(session, url):
    async with session.get(url) as res:
        content = await res.text()
        soup = BeautifulSoup(content, "lxml")
        soup_str = str(soup)
        soup_bytes = bytes(soup_str, encoding="utf8")
        lxml_data = html.fromstring(soup_bytes)
        return lxml_data
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "lxml")
    soup_str = str(soup)
    soup_bytes = bytes(soup_str, encoding="utf8")
    lxml_data = html.fromstring(soup_bytes)
    return lxml_data

async def fetch_pdf(session, url):
    pdf_url = url.replace("abs", "pdf")
    async with session.get(pdf_url) as res:
        pdf_data = await res.read()
        return res.status, pdf_data
    
async def fetch_data(session, siteInfo):
    arxiv_data = await fetch_arxiv(session, siteInfo["url"])
    pdf_status, pdf_data = await fetch_pdf(session, siteInfo["url"])
    return siteInfo, arxiv_data, pdf_status, pdf_data

async def load_site_contents(siteData):
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, siteInfo) for siteInfo in siteData]
        results = await asyncio.gather(*tasks)
        
        for siteInfo, arxiv_data, pdf_status, pdf_data in results:
            #Title
            title = arxiv_data.xpath("//meta[@property='og:title']/@content")[0]
            
            #Author
            author = arxiv_data.xpath("//div[@class='authors']/a/text()")
            authors = ", ".join(author)
            
            #conference 要確認
            if arxiv_data.xpath("//td[@class='tablecell comments mathjax']/text()"):
                conf_text = arxiv_data.xpath("//td[@class='tablecell comments mathjax']/text()")[0]
                if conf_text.startswith('Accepted by '):
                    conference = conf_text[len('Accepted by '):]
                else:
                    conference = conf_text
            else:
                conference = None
            
            #pages
            if pdf_status == 200:
                pdf_file = BytesIO(pdf_data)
                pdf_reader = PdfFileReader(pdf_file)
                pages = pdf_reader.getNumPages()      
            else:
                pages = None
            
            #date
            dateline = arxiv_data.xpath("//div[@class='dateline']/text()")[0].strip()
            date_part = dateline.strip('[]').replace('Submitted on ', '')
            date_obj = datetime.strptime(date_part, '%d %b %Y')
            date = date_obj.strftime('%y%m%d')
            
            #abstract
            abstract = arxiv_data.xpath("//meta[@property='og:description']/@content")[0]
            
            #cite num 要確認
            cite_num = None
            
            #submitted
            if arxiv_data.xpath("//td[@class='tablecell comments mathjax']/text()"):
                submitted = True
            else:
                submitted = False
            
            # エントリーを追加する
            add_entry(siteInfo["url"], title, authors, conference, pages, date, abstract, cite_num, submitted, siteInfo["relevant_no"])


# エントリーを追加する関数
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


#MAIN
load_dotenv()
asyncio.run(load_site_contents(test_data))

print()
