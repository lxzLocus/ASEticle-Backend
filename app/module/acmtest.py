from acm import execute
import asyncio
# from acm import load_acm_contents

sitedata = [
    {
        'url': 'https://dl.acm.org/doi/abs/10.1145/3512345', 
        'relevant_no': 0, 
        'cite_num': 161
    },
    {
        'url': 'https://dl.acm.org/doi/abs/10.1145/3133956.3134020', 
        'relevant_no': 2, 
        'cite_num': 802
    },
    {   
        'url': 'https://dl.acm.org/doi/abs/10.1145/1375581.1375607', 
        'relevant_no': 5, 
        'cite_num': 733
    },
    {
        'url': 'https://dl.acm.org/doi/abs/10.1145/3293882.3330576', 
        'relevant_no': 14, 
        'cite_num': 161
    }, 
    {
        'url': 'https://dl.acm.org/doi/abs/10.1145/2976749.2978428', 
        'relevant_no': 15, 
        'cite_num': 1015
    }
]

# sitedata = [
#     {'url': 'https://ieeexplore.ieee.org/abstract/document/8371326/', 
#      'relevant_no': 1, 
#      'cite_num': 276
#     },
#     {'url': 'https://ieeexplore.ieee.org/abstract/document/8863940/', 
#      'relevant_no': 4, 
#      'cite_num': 473
#     },
#     {'url': 'https://ieeexplore.ieee.org/abstract/document/9166552/', 
#      'relevant_no': 7, 
#      'cite_num': 138
#     },
#     {'url': 'https://ieeexplore.ieee.org/abstract/document/8839290/', 
#      'relevant_no': 8, 
#      'cite_num': 231
#     },
#     {'url': 'https://ieeexplore.ieee.org/abstract/document/8424642/', 
#      'relevant_no': 9, 
#      'cite_num': 130
#     }
# ]

# print(load_acm_contents(sitedata))

# async def scraping_main(sitedata):
#     a = await load_arxiv_contents(sitedata)

#     return a

# print(asyncio.run(scraping_main(sitedata)))

async def scraping_main(sitedata):
    a = await execute(sitedata)

    return a

print(asyncio.run(scraping_main(sitedata)))