import matching
import time

if __name__ == '__main__':
    # 機能テスト
    entry = {
        "url": "urlToPaper",
        "title": "Research About Super Resolution",
        "author": "Jane Doe, John Smith, Gonbee Nnashi",
        "conference": None,
        "pages": 99,
        "date": "20990804",
        "abstract": [
            "Super resolution is a technique that generates a high-resolution image from a low-resolution image. In this paper, we propose a new method for super resolution."
        ],
        "cite_num": 1000,
        "submitted": False,
        "relevant_no": 0
    }

    test=None

    # if test!=None and test!={}: 
    #     if test["conference"] != None:
    #         print(test["conference"])
            
    # start = time.perf_counter()
    # print(matching.match_conference_fuzzy(entry))
    # end = time.perf_counter()
    # print(f"Time: {end - start} s")
