import polars as pl
import json
import asyncio


async def match(entries) -> None:
    serch_value = entries["conference"]
    
    conf_rank = ( #会議名とtier情報の照合,会議名が一致する場合は正式名称に修正したものを取得
        pl.read_csv("data/conf_n_journal_list.csv")
        .filter(pl.col("title").is_in([serch_value]) | pl.col("acronym").is_in([serch_value]))
        .select(["title", "tier"])
    )
    
    #変換
    conf_info = conf_rank.to_dict()
    conf_name = conf_info["title"].to_list()
    conf_tier = conf_info["tier"].to_list()
    if len(conf_name) == 0:
        conf_name = [""]
        conf_tier = [-1]

    fix_entry(entries, conf_name[0], conf_tier[0])


def fix_entry(entries, fixed_conf_name, tier):
    # 引数のクエリに対して、(可能であれば)会議名の修正とtierデータを追加
    if fixed_conf_name != "":
        entries["conference"] = fixed_conf_name
    entries["tier"] = tier

# MAIN
def match_conference(entries):
    asyncio.run(match(entries))

    return json.dumps(entries, indent=4) #json形式で出力
