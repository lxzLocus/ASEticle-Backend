import requests
from bs4 import BeautifulSoup
import random
import time

def scrape_googlescholar(query):
    # 指定されたドメインのみを許可
    allowed_domains = ["https://arxiv.org/", "https://ieeexplore.ieee.org/", "https://www.sciencedirect.com/", "https://dl.acm.org/"]

    # 取得したURLを格納するリスト
    url_list = []

    for i in range(6):
        if i == 0:
            # Google Scholarの検索結果ページのURL
            search_query = 'https://scholar.google.com/scholar?q=' + query
        else:
            # Google Scholarの検索結果ページのURL
            search_query = 'https://scholar.google.com/scholar?q=' + query + '&start=' + str(i) + '0'

        # HTTPリクエストヘッダーの設定
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # リクエストを送信
        response = requests.get(search_query, headers=headers)

        # ステータスコードを確認
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 論文のURLを抽出し、指定されたドメインのみをリストに追加
            for entry in soup.find_all('h3', class_='gs_rt'):
                link = entry.find('a')
                if link:
                    url = link['href']
                    # 指定されたドメインのURLのみをリストに追加し、/pdf/を含まない
                    if any(domain in url for domain in allowed_domains) and '/pdf/' not in url:
                        url_list.append(url)
                else:
                    print("No URL found for this entry.")
                
            # 適切な間隔を空ける
            time.sleep(random.uniform(1, 5))
        else:
            print(f"Failed to retrieve search results. Status code: {response.status_code}")

    # 辞書型のリストを作成
    all_array = [{"url": url, "relevant_no": index} for index, url in enumerate(url_list)]

    # リストを分ける
    arxiv_array = [entry for entry in all_array if allowed_domains[0] in entry["url"]]
    ieee_array = [entry for entry in all_array if allowed_domains[1] in entry["url"]]
    sciencedirect_array = [entry for entry in all_array if allowed_domains[2] in entry["url"]]
    acm_array = [entry for entry in all_array if allowed_domains[3] in entry["url"]]

    return arxiv_array, ieee_array, sciencedirect_array, acm_array

# # テスト
# if __name__ == "__main__":
#     query = "machine+learning"
#     arxiv, ieee, sciencedirect, acm = scrape_googlescholar(query)
#     print("arxiv_array:", arxiv)
#     print("ieee_array:", ieee)
#     print("sciencedirect_array:", sciencedirect)
#     print("acm_array:", acm)

# 使用例
# from googlescholar_scraper import scrape_googlescholar
# query = "deep learning"
# arxiv, ieee, sciencedirect, acm = scrape_googlescholar(query)
# print("arxiv_array:", arxiv)
# print("ieee_array:", ieee)
# print("sciencedirect_array:", sciencedirect) 
# print("acm_array:", acm)
