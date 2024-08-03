# from arxiv import execute
import asyncio
from ieee import ieee_execute

# sitedata = [
#     {
#         "url" : "https://arxiv.org/abs/2403.00448",
#         "relevant_no" : 1,
#         'cite_num': 276
#     },
#     {
#         "url" : "https://arxiv.org/abs/2406.05621",
#         "relevant_no" :2,
#         'cite_num': 473
#     },
#     {
#         "url" : "https://arxiv.org/abs/2404.05598",
#         "relevant_no" : 3,
#         'cite_num': 138
#     },
#     {
#         "url" : "https://arxiv.org/abs/2212.07475",
#         "relevant_no" : 4,
#         'cite_num': 231
#     },
#     {
#         "url" : "https://arxiv.org/abs/2404.05598",
#         "relevant_no" : 5,
#         'cite_num': 130
#     }
# ]

sitedata = [
    {'url': 'https://ieeexplore.ieee.org/abstract/document/8371326/', 
     'relevant_no': 1, 
     'cite_num': 276
    },
    {'url': 'https://ieeexplore.ieee.org/abstract/document/8863940/', 
     'relevant_no': 4, 
     'cite_num': 473
    },
    {'url': 'https://ieeexplore.ieee.org/abstract/document/9166552/', 
     'relevant_no': 7, 
     'cite_num': 138
    },
    {'url': 'https://ieeexplore.ieee.org/abstract/document/8839290/', 
     'relevant_no': 8, 
     'cite_num': 231
    },
    {'url': 'https://ieeexplore.ieee.org/abstract/document/8424642/', 
     'relevant_no': 9, 
     'cite_num': 130
    }
]

# print(load_arxiv_contents(sitedata))

# async def scraping_main(sitedata):
#     a = await load_arxiv_contents(sitedata)

#     return a

# print(asyncio.run(scraping_main(sitedata)))

async def scraping_main(sitedata):
    a = await ieee_execute(sitedata)

    return a

print(asyncio.run(scraping_main(sitedata)))