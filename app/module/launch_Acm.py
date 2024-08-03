from Cacm import execute
import asyncio

apiRes =  [  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3512345', 'relevant_no': 0, 'cite_num': 161}, 
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3133956.3134020', 'relevant_no': 2, 'cite_num': 802},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/1375581.1375607', 'relevant_no': 5, 'cite_num': 733},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3293882.3330576', 'relevant_no': 14, 'cite_num': 161},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/2976749.2978428', 'relevant_no': 15, 'cite_num': 1015},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3460120.3484596', 'relevant_no': 18, 'cite_num': 62},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3460319.3464795', 'relevant_no': 21, 'cite_num': 81},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3106237.3106295', 'relevant_no': 22, 'cite_num': 351},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3538644', 'relevant_no': 24, 'cite_num': 36},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3510003.3510174', 'relevant_no': 25, 'cite_num': 52},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3236024.3264835', 'relevant_no': 27, 'cite_num': 282},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3377811.3380396', 'relevant_no': 28, 'cite_num': 130},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3133956.3134046', 'relevant_no': 29, 'cite_num': 148},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3213846.3213848', 'relevant_no': 32, 'cite_num': 167},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3623375', 'relevant_no': 33, 'cite_num': 9},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3360600', 'relevant_no': 34, 'cite_num': 76},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/2970276.2970316', 'relevant_no': 35, 'cite_num': 128},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/2508859.2516736', 'relevant_no': 36, 'cite_num': 251},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3314221.3314651', 'relevant_no': 37, 'cite_num': 64},  
    {'url': 'https://dl.acm.org/doi/abs/10.1145/3238147.3238177', 'relevant_no': 38, 'cite_num': 698}
]

async def main():
    print(await execute(apiRes))
    
asyncio.run(main())