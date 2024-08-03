"Cacmのテスト"
import Cacm
import asyncio

if __name__ == "__main__":
    param = [
        {
            "url": "https://dl.acm.org/doi/10.1145/3372297.3417280",
            "relevant_no": 1,
            "cite_num": 0,
        },
        {
            "url": "https://dl.acm.org/doi/10.1145/3372297.3417281",
            "relevant_no": 2,
            "cite_num": 1,
        },
    ]
    entries= asyncio.run(Cacm.execute(param))
    print(entries)
    print("Cacm test passed")