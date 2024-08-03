from app.module import execute, load_arxiv_contents, load_acm_contents
import asyncio
import aiohttp
from dotenv import load_dotenv


import sys
import os

# カレントディレクトリを設定
sys.path.append(os.path.join(os.path.dirname(__file__), 'module'))

# モジュールをインポート
from Arxiv_useclass import execute

load_dotenv()
# SerpApiのAPIキーを環境変数から取得
api_keys = [value for key, value in os.environ.items() if key.startswith("SERP_APIKEY")]

query ="machine+learning"

# 指定されたドメインのみを許可
allowed_domains = ["https://dl.acm.org/", "https://arxiv.org/", "https://ieeexplore.ieee.org/", "https://www.sciencedirect.com/"]
# 04
async def fetch_results(session, query, start, index):

    for api_key in api_keys:
        params = {
            "engine": "google_scholar",
            "q": query,
            "start": start,
            "api_key": api_key,
            "num": 20
        }
    
        async with session.get("https://serpapi.com/search?", params=params) as response:
            result = await response.json()
            if response.status != 200:#'error' in result and 'Rate limit reached' in result['error']:
                print(f"APIキー {api_key} の使用中にエラーが発生しました。次のAPIキーを試します。")
            else:
                return (index, result)

    raise Exception("すべてのAPIキーが回数制限に達しました")

# 03
async def search_googlescholar(query):
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        # for i in range(6):
        #     start = i * 20
        #     tasks.append(fetch_results(session, query, start, i))
        
        # results = await asyncio.gather(*tasks)
        results = [{'url': 'https://dl.acm.org/doi/abs/10.1145/3512345', 'relevant_no': 0, 'cite_num': 161}, {'url': 'https://ieeexplore.ieee.org/abstract/document/8371326/', 'relevant_no': 1, 'cite_num': 276}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3133956.3134020', 'relevant_no': 2, 'cite_num': 802}, {'url': 'https://www.sciencedirect.com/science/article/pii/S0167404818300658', 'relevant_no': 3, 'cite_num': 152}, {'url': 'https://ieeexplore.ieee.org/abstract/document/8863940/', 'relevant_no': 4, 'cite_num': 473}, {'url': 'https://dl.acm.org/doi/abs/10.1145/1375581.1375607', 'relevant_no': 5, 'cite_num': 733}, {'url': 'https://ieeexplore.ieee.org/abstract/document/8418632/', 'relevant_no': 6, 'cite_num': 380}, {'url': 'https://ieeexplore.ieee.org/abstract/document/9166552/', 'relevant_no': 7, 'cite_num': 138}, {'url': 'https://ieeexplore.ieee.org/abstract/document/8839290/', 'relevant_no': 8, 'cite_num': 231}, {'url': 'https://ieeexplore.ieee.org/abstract/document/8424642/', 'relevant_no': 9, 'cite_num': 130}, {'url': 'https://ieeexplore.ieee.org/abstract/document/8418631/', 'relevant_no': 10, 'cite_num': 483}, {'url': 'https://ieeexplore.ieee.org/abstract/document/8115618/', 'relevant_no': 11, 'cite_num': 464}, {'url': 'https://ieeexplore.ieee.org/abstract/document/7163057/', 'relevant_no': 12, 'cite_num': 331}, {'url': 'https://arxiv.org/abs/1812.00140', 'relevant_no': 13, 'cite_num': 24}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3293882.3330576', 'relevant_no': 14, 'cite_num': 161}, {'url': 'https://dl.acm.org/doi/abs/10.1145/2976749.2978428', 'relevant_no': 15, 'cite_num': 1015}, {'url': 'https://ieeexplore.ieee.org/abstract/document/8835316/', 'relevant_no': 16, 'cite_num': 165}, {'url': 'https://ieeexplore.ieee.org/abstract/document/1423963/', 'relevant_no': 17, 'cite_num': 385}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3460120.3484596', 'relevant_no': 18, 'cite_num': 62}, {'url': 'https://ieeexplore.ieee.org/abstract/document/8811923/', 'relevant_no': 19, 'cite_num': 247}, {'url': 'https://ieeexplore.ieee.org/abstract/document/7958599/', 'relevant_no': 20, 'cite_num': 397}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3460319.3464795', 'relevant_no': 21, 'cite_num': 81}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3106237.3106295', 'relevant_no': 22, 'cite_num': 351}, {'url': 'https://ieeexplore.ieee.org/abstract/document/5070546/', 'relevant_no': 23, 'cite_num': 497}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3538644', 'relevant_no': 24, 'cite_num': 36}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3510003.3510174', 'relevant_no': 25, 'cite_num': 52}, {'url': 'https://ieeexplore.ieee.org/abstract/document/8418633/', 'relevant_no': 26, 'cite_num': 630}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3236024.3264835', 'relevant_no': 27, 'cite_num': 282}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3377811.3380396', 'relevant_no': 28, 'cite_num': 130}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3133956.3134046', 'relevant_no': 29, 'cite_num': 148}, {'url': 'https://ieeexplore.ieee.org/abstract/document/5770635/', 'relevant_no': 30, 'cite_num': 112}, {'url': 'https://ieeexplore.ieee.org/abstract/document/7839812/', 'relevant_no': 31, 'cite_num': 162}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3213846.3213848', 'relevant_no': 32, 'cite_num': 167}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3623375', 'relevant_no': 33, 'cite_num': 9}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3360600', 'relevant_no': 34, 'cite_num': 76}, {'url': 'https://dl.acm.org/doi/abs/10.1145/2970276.2970316', 'relevant_no': 35, 'cite_num': 128}, {'url': 'https://dl.acm.org/doi/abs/10.1145/2508859.2516736', 'relevant_no': 36, 'cite_num': 251}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3314221.3314651', 'relevant_no': 37, 'cite_num': 64}, {'url': 'https://dl.acm.org/doi/abs/10.1145/3238147.3238177', 'relevant_no': 38, 'cite_num': 698}, {'url': 'https://ieeexplore.ieee.org/abstract/document/10018241/', 'relevant_no': 39, 'cite_num': 41}]
        # インデックスでソートして順序を保つ
        results.sort(key=lambda x: x[0])  
        
        url_list = []
        cite_num_list = [] # cite_num（被引用数: apiでいうtotal）とrelevant_noを格納する辞書
        for _, result in results:
            for entry in result.get("organic_results", []):
                link = entry.get("link") 
                cited_by = entry.get('inline_links', {}).get('cited_by', {})
                cite_num = cited_by.get('total')

                if link:
                    # 指定されたドメインのURLのみをリストに追加し、/pdf/を含まない
                    if any(domain in link for domain in allowed_domains) and '/pdf/' not in link:
                        url_list.append(link)
                        cite_num_list.append(cite_num)
        
        # 辞書型のリストを作成
        all_array = [{"url": url, "relevant_no": index} for index, url in enumerate(url_list)]
        cite_num_list = [{"citation_count": cite_count, "relevant_no": index} for index, cite_count in enumerate(cite_num_list)]
        await update_cite_num(all_array, cite_num_list)
        # リストを分ける
        acm_array = [entry for entry in all_array if allowed_domains[0] in entry["url"]]
        arxiv_array = [entry for entry in all_array if allowed_domains[1] in entry["url"]]
        ieee_array = [entry for entry in all_array if allowed_domains[2] in entry["url"]]
        sciencedirect_array = [entry for entry in all_array if allowed_domains[3] in entry["url"]]
        
        return acm_array, arxiv_array, ieee_array, sciencedirect_array, cite_num_list


#05
#被引用数を上書きする処理（all_data:各サイトのスクレイピング処理の返り値を配列にまとめたもの,new_cite:APIによって取得した被引用数と関連度を格納した配列）
#all_dataの関連度とnew_citeの関連度が同じならcite_numを上書きする
async def update_cite_num(all_data, new_cite):
    await asyncio.sleep(0)  # 非同期処理をシミュレート
    for update in new_cite:
        for data in all_data:
            # データがリストの場合
            if isinstance(data, list):
                for item in data:
                    if item['relevant_no'] == update['relevant_no']:
                        item['cite_num'] = update['citation_count']
            # データが辞書の場合
            elif isinstance(data, dict):
                if data['relevant_no'] == update['relevant_no']:
                    data['cite_num'] = update['citation_count']

#02
async def scraping_main(query):
    acm, arxiv, ieee, sciencedirect ,citation_count= await search_googlescholar(query) #テスト用、実装時に消す　acm_test,arxiv_test, ieee_test, sciencedirect_test ,citation_count_test
    #print(ieee)
    result = []
    #result.append(await load_acm_contents(acm))
    result.append(await execute(arxiv))
    result.append(await execute(ieee))

    await update_cite_num(result, citation_count) #被引用数の上書き処理
    print("all_data",result)

    #matchingを呼び出す処理を付け加える
    return result

#テスト用
if __name__ == "__main__":
    query = "RESTAPI"
    asyncio.run(scraping_main(query)) 