import json
import os
import itertools
import multiprocessing

import crawler

num_process = 8

# configs
with open(os.path.dirname(os.path.abspath(__file__)) + "/config/servers.json", "r", encoding="utf-8") as j:
    servers = json.load(j)

with open(os.path.dirname(os.path.abspath(__file__)) + "/config/item_names.json", "r", encoding="utf-8") as j:
    item_names = json.load(j)

total_works = list(itertools.product(servers, item_names))[:16]


if __name__ == "__main__":
    ### multiprocessing.Pool Issue 
    ### Pool must be in if __name__ == "__main__" scope.
    with multiprocessing.Pool(num_process) as p:
        p.map(crawler.main, total_works)
