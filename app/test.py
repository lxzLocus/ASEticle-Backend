import matching
import time
import tracemalloc

if __name__ == '__main__':
    # 機能・性能テスト
    entry = {
        "url": "urlToPaper",
        "title": "Research About Super Resolution",
        "author": "Jane Doe, John Smith, Gonbee Nnashi",
        "conference": "ICSE",
        "pages": 99,
        "date": "20990804",
        "abstract": [
            "Super resolution is a technique that generates a high-resolution image from a low-resolution image. In this paper, we propose a new method for super resolution."
        ],
        "cite_num": 1000,
        "submitted": False,
        "relevant_no": 0
    }

    start = time.perf_counter() #計測開始
    print(matching.match_conference(entry))
    end = time.perf_counter() #計測終了
    print(f"Time: {end - start} s")
