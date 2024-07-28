import asyncio
import aiohttp

# テスト
if __name__ == "__main__":
    test_json = {
    'url': 'https://arxiv.org/abs/2403.00448',
    'title': 'When Large Language Models Confront Repository-Level Automatic Program Repair: How Well They Done?',
    'author': 'Yuxiao Chen, Jingzheng Wu, Xiang Ling, Changjiang Li, Zhiqing Rui, Tianyue Luo, Yanjun Wu',
    'conference': '2024 IEEE/ACM 46th International Conference on Software Engineering: Companion Proceedings (ICSE-Companion)',
    'pages': 13,
    'date': '240301',
    'abstract': 'In recent years, large language models (LLMs) have demonstrated substantial potential in addressing automatic program repair (APR) tasks. However, the current evaluation of these models for APR tasks focuses solely on the limited context of the single function or file where the bug is located, overlooking the valuable information in the repository-level context. This paper investigates the performance of popular LLMs in handling repository-level repair tasks. We introduce RepoBugs, a new benchmark comprising 124 typical repository-level bugs from open-source repositories. Preliminary experiments using GPT3.5 based on the function where the error is located, reveal that the repair rate on RepoBugs is only 22.58%, significantly diverging from the performance of GPT3.5 on function-level bugs in related studies. This underscores the importance of providing repository-level context when addressing bugs at this level. However, the repository-level context offered by the preliminary method often proves redundant and imprecise and easily exceeds the prompt length limit of LLMs. To solve the problem, we propose a simple and universal repository-level context extraction method (RLCE) designed to provide more precise context for repository-level code repair tasks. Evaluations of three mainstream LLMs show that RLCE significantly enhances the ability to repair repository-level bugs. The improvement reaches a maximum of 160% compared to the preliminary method. Additionally, we conduct a comprehensive analysis of the effectiveness and limitations of RLCE, along with the capacity of LLMs to address repository-level bugs, offering valuable insights for future research.',
    'cite_num': 3,
    'submitted': True,
    'relevant_no': 1
    }
    query = "machine+learning"

# SerpApiのAPIキーを環境変数から取得
api_key = ""

# 指定されたドメインのみを許可
allowed_domains = ["https://dl.acm.org/", "https://arxiv.org/", "https://ieeexplore.ieee.org/", "https://www.sciencedirect.com/"]

# 02
async def fetch_results(session, query, start, index):
    params = {
        "engine": "google_scholar",
        "q": query,
        "start": start,
        "api_key": api_key,
        "num": 20
    }
    
    async with session.get("https://serpapi.com/search?", params=params) as response:
        result = await response.json()
        print(result)
        return (index, result)

# 01
async def search_googlescholar(query):
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for i in range(6):
            start = i * 20
            tasks.append(fetch_results(session, query, start, i))
        
        results = await asyncio.gather(*tasks)
        # インデックスでソートして順序を保つ
        results.sort(key=lambda x: x[0])  
        
        url_list = []
        cite_num_list = [] # cite_num（被引用数: apiでいうtotal）とrelevant_noを格納する辞書
        for _, result in results:
            for entry in result.get("organic_results", []):
                link = entry.get("link") 
                ################################
                # [追加]被引用数を取得するコード
                # api keyが使えるか使えないかの判定も追加する#
                ################################
                cited_by = entry.get('inline_links', {}).get('cited_by', {})
                cite_num = cited_by.get('total')

                if link:
                    # 指定されたドメインのURLのみをリストに追加し、/pdf/を含まない
                    if any(domain in link for domain in allowed_domains) and '/pdf/' not in link:
                        url_list.append(link)
                        #######################################
                        # [追加]被引用数をcite_num_listにappend#
                        #######################################
                        cite_num_list.append(cite_num)
        
        # 辞書型のリストを作成
        all_array = [{"url": url, "relevant_no": index} for index, url in enumerate(url_list)]
        cite_num_list = [{"citation_count": cite_count, "relevant_no": index} for index, cite_count in enumerate(cite_num_list)]
        
        # リストを分ける
        acm_array = [entry for entry in all_array if allowed_domains[0] in entry["url"]]
        arxiv_array = [entry for entry in all_array if allowed_domains[1] in entry["url"]]
        ieee_array = [entry for entry in all_array if allowed_domains[2] in entry["url"]]
        sciencedirect_array = [entry for entry in all_array if allowed_domains[3] in entry["url"]]
        
        return acm_array, arxiv_array, ieee_array, sciencedirect_array, cite_num_list

async def update_citations(json, citation_count):
    tasks = []
    for citation in citation_count:
        if citation['relevant_no'] == json['relevant_no']:
            task = asyncio.create_task(update_cite_num(citation, json['cite_num']))
            tasks.append(task)
    await asyncio.gather(*tasks)

async def update_cite_num(citation, new_cite_num):
    await asyncio.sleep(0)  # 非同期処理をシミュレート
    citation['cite_num'] = new_cite_num

def main(query,json):
    acm, arxiv, ieee, sciencedirect ,citation_count= asyncio.run(search_googlescholar(query))
    print("acm_array:", acm)
    print("arxiv_array:", arxiv)
    print("ieee_array:", ieee)
    print("sciencedirect_array:", sciencedirect)
    print("citation_array:",citation_count)

    asyncio.run(update_citations(json, citation_count))

main(query,test_json)


# 使用例
# from googlescholar_searcher import search_googlescholar
# query = "deep learning"
# acm, arxiv, ieee, sciencedirect = asyncio.run(search_googlescholar(query))
# print("acm_array:", acm)
# print("arxiv_array:", arxiv)
# print("ieee_array:", ieee)
# print("sciencedirect_array:", sciencedirect) 
