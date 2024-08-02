from app.module.Arxiv_useclass import execute
import asyncio

apiRes = [{'url': 'https://arxiv.org/abs/1812.00140', 'relevant_no': 13, 'cite_num': 24}]

async def main():
    print(await execute(apiRes))
    
asyncio.run(main())