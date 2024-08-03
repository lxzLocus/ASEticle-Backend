import polars as pl
from rapidfuzz import process
import json
import asyncio
import numpy as np

        
async def entries_match (parent_entries):
    df = pl.read_csv("data/conf_n_journal_list.csv")
    check_conf_title = df["title"]
    check_conf_acronym = df["acronym"]
    entries_conf = []
    
    for entry in parent_entries:
        entries_conf.append(entry["conference"])
    t_scores = process.cdist(check_conf_title, entries_conf, score_cutoff=80)
    a_scores = process.cdist(check_conf_acronym, entries_conf, score_cutoff=80)
    
    for i, entry in enumerate(parent_entries):
        t_score = t_scores[i]
        a_score = a_scores[i]
        t_max = np.max(t_score)
        a_max = np.max(a_score)
        if t_max == 0 and a_max == 0:
            entry["tier"] = -1
        elif t_max > a_max:
            entry["conference"] = df["title"][t_score.index(t_max)]
            entry["tier"] = df["tier"][t_score.index(t_max)]
        else:
            entry["conference"] = df["title"][a_score.index(a_max)]
            entry["tier"] = df["tier"][a_score.index(a_max)]


async def match(entry) -> None:
    search_value = fetch_conf_name(entry)
    
    if search_value != "":
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
    else:
        conf_name = [""]
        conf_tier = [-1]

    fix_entry(entry, conf_name[0], conf_tier[0])
    
async def fuzzy_match(entry) -> None:
    search_value = fetch_conf_name(entry)

    if search_value != "":
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
    else:
        conf_name = [""]
        conf_tier = [-1]
    
    fix_entry(entry, conf_name[0], conf_tier[0])
    

def fetch_conf_name(entry) -> str:
    if entry!=None and entry!={}: 
        if entry["conference"] != None:
            return entry["conference"]
    
    return ""

def fuzzy_match_score(search_value, series):
    ans = process.extractOne(search_value, series)
    if ans[1] < 90:
        return "hoge zxqjb"
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

def eager_match_conferences(entries):
    for entry in entries:
        asyncio.run(fuzzy_match(entry))

    return json.dumps(entries, indent=4) #json形式で出力

def one_shot_match_conferences(entries):
    asyncio.run(entries_match(entries))

    return json.dumps(entries, indent=4) #json形式で出力