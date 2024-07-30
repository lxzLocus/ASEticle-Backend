import polars as pl
from rapidfuzz import fuzz, process
import json
import asyncio


class ConferenceMatcher:
    def __init__(self):
        self.df = pl.scan_csv("data/conf_n_journal_list.csv")
        
    def match(self, entries):
        for entry in entries:
            pass

# async def match(entry) -> None:
#     search_value = entry["conference"]
    
#     conf_rank = ( #会議名とtier情報の照合,会議名が一致する場合は正式名称に修正したものを取得
#         pl.read_csv("data/conf_n_journal_list.csv")
#         .filter(pl.col("title").is_in([search_value]) | pl.col("acronym").is_in([search_value]))
#         .select(["title", "tier"])
#     )
    
#     #変換
#     conf_info = conf_rank.to_dict()
#     conf_name = conf_info["title"].to_list()
#     conf_tier = conf_info["tier"].to_list()
#     if len(conf_name) == 0:
#         conf_name = [""]
#         conf_tier = [-1]

#     fix_entry(entry, conf_name[0], conf_tier[0])

async def match(entry) -> None:
    search_value = entry["conference"]
    
    conf_rank = ( #会議名とtier情報の照合,会議名が一致する場合は正式名称に修正したものを取得
        pl.read_csv("data/conf_n_journal_list.csv")
        .filter(pl.col("title").str.contains(search_value) | pl.col("acronym").str.contains(search_value))
        .select(["title", "tier"])
    )
    
    #変換
    conf_info = conf_rank.to_dict()
    conf_name = conf_info["title"].to_list()
    conf_tier = conf_info["tier"].to_list()
    if len(conf_name) == 0:
        conf_name = [""]
        conf_tier = [-1]

    fix_entry(entry, conf_name[0], conf_tier[0])
    
async def fuzzy_match(entry) -> None:
    search_value = entry["conference"]
    
    conf_rank = (
        pl.read_csv("data/conf_n_journal_list.csv")
        .filter(
            (pl.col("title").str
            .contains(pl.col("title")
            .map_batches(lambda s: fuzzy_match_score(search_value, s)))
            ) |
            (pl.col("acronym").str
            .contains(pl.col("acronym")
            .map_batches(lambda s: fuzzy_match_score(search_value, s)))
            )
        )
        .select(["title", "tier"])
    )
    
    #変換
    conf_info = conf_rank.to_dict()
    conf_name = conf_info["title"].to_list()
    conf_tier = conf_info["tier"].to_list()
    if len(conf_name) == 0:
        conf_name = [""]
        conf_tier = [-1]
    
    fix_entry(entry, conf_name[0], conf_tier[0])

def fuzzy_match_score(search_value, series):
    ans = process.extractOne(search_value, series)
    print("extract:" + str(ans))
    # if ans[1] < 90:
    #     return 0
    # return ans[2]
    if ans[1] < 90:
        return "hoge"
    return ans[0]

def fix_entry(entry, fixed_conf_name, tier):
    # 引数のクエリに対して、(可能であれば)会議名の修正とtierデータを追加
    if fixed_conf_name != "":
        entry["conference"] = fixed_conf_name
    entry["tier"] = tier


# MAIN
def match_conference(entry):
    asyncio.run(match(entry))

    return json.dumps(entry, indent=4) #json形式で出力

def match_conference_fuzzy(entry):
    asyncio.run(fuzzy_match(entry))

    return json.dumps(entry, indent=4) #json形式で出力