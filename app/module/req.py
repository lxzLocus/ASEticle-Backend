from arxiv import load_arxiv_contents

sitedata = [
    {
        "url" : "https://arxiv.org/abs/2403.00448",
        "relevant_no" : 1
    },
    {
        "url" : "https://arxiv.org/abs/2406.05621",
        "relevant_no" :2
    },
    {
        "url" : "https://arxiv.org/abs/2404.05598",
        "relevant_no" : 3
    },
    {
        "url" : "https://arxiv.org/abs/2212.07475",
        "relevant_no" : 4
    },
    {
        "url" : "https://arxiv.org/pdf/2208.12743",
        "relevant_no" : 5
    }
]
    
print(load_arxiv_contents(sitedata))