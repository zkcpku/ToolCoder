import json
import re
from rank_bm25 import BM25Okapi

def clean_string(s):
    s = s.lower().split()
    s = [re.sub('\W*', '', e) for e in s]
    s = [e for e in s if len(e) > 0]
    s = " ".join(s)
    return s

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)
def init_bm25(corpus):
    tokenized_corpus = [doc.split(" ") for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    return bm25
def merge_dict(d1, d2):
    d = {}
    for k,v in d1.items():
        d[k] = v
    for k,v in d2.items():
        d[k] = v
    return d

BEATNUM = load_json("doc/beatnum_doc2api.json")
MONKEY = load_json("doc/monkey_doc2api.json")
TOTAL_dict = merge_dict(BEATNUM, MONKEY)

BEATNUM_bm25 = init_bm25(list(BEATNUM.keys()))
MONKEY_bm25 = init_bm25(list(MONKEY.keys()))
TOTAL_bm25 = init_bm25(list(TOTAL_dict.keys()))


def search_in_bm25(query, search_base):
    query = clean_string(query)
    tokenized_query = query.split(" ")
    if search_base == "beatnum":
        bm25 = BEATNUM_bm25
        corpus = list(BEATNUM.keys())
    elif search_base == "monkey":
        bm25 = MONKEY_bm25
        corpus = list(MONKEY.keys())
    elif search_base == "total":
        bm25 = TOTAL_bm25
        corpus = list(TOTAL_dict.keys())
    else:
        return None
    search_rst = bm25.get_top_n(tokenized_query, corpus, n=1)
    if len(search_rst) == 0:
        return None
    else:
        return TOTAL_dict[search_rst[0]]
