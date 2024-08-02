from acm import load_acm_contents
import asyncio

sitedata = [
    {
        "url" : "https://dl.acm.org/doi/10.1145/3605157.3605176",
        "relevant_no" : 1
    },
    {
        "url" : "https://dl.acm.org/doi/10.1145/3587158",
        "relevant_no" :2
    },
    {
        "url" : "https://dl.acm.org/doi/10.1145/3605157.3605173",
        "relevant_no" : 3
    },
    {
        "url" : "https://dl.acm.org/doi/10.1145/3611668",
        "relevant_no" : 4
    },
    {
        "url" : "https://dl.acm.org/doi/10.1145/3643778",
        "relevant_no" : 5
    }
]

print(load_acm_contents(sitedata))

# async def scraping_main(sitedata):
#     a = await load_acm_contents(sitedata)

#     return a

# print(asyncio.run(scraping_main(sitedata)))