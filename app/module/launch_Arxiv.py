from Carxiv import execute
import asyncio

apiRes =  [
    {
        "url" : "https://arxiv.org/abs/2403.00448",
        "relevant_no" : 1,
        'cite_num': 276
    },
    {
        "url" : "https://arxiv.org/abs/2406.05621",
        "relevant_no" :2,
        'cite_num': 473
    },
    {
        "url" : "https://arxiv.org/abs/2404.05598",
        "relevant_no" : 3,
        'cite_num': 138
    },
    {
        "url" : "https://arxiv.org/abs/2212.07475",
        "relevant_no" : 4,
        'cite_num': 231
    },
    {
        "url" : "https://arxiv.org/pdf/2208.12743",
        "relevant_no" : 5,
        'cite_num': 130
    }
]

async def main():
    print(await execute(apiRes))
    
asyncio.run(main())