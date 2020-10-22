import datetime
import json
import os
from itertools import product
import multiprocessing

import crawler

num_process = 8

# configs
with open(os.path.dirname(os.path.abspath(__file__)) + "/config/servers.json", "r", encoding="utf-8") as j:
    servers = json.load(j)

with open(os.path.dirname(os.path.abspath(__file__)) + "/config/item_names.json", "r", encoding="utf-8") as j:
    item_names = json.load(j)

total_works = list(product(servers, item_names))[:8]        ###################


if __name__ == "__main__":
    delta_hour = 0

    while True:
        current_hour = datetime.datetime.now().minute       ###############

        if delta_hour != current_hour:
            ### multiprocessing.Pool Issue 
            ### Pool must be in if __name__ == "__main__" scope.
            with multiprocessing.Pool(num_process) as p:
                p.map(crawler.main, total_works)

        delta_hour = current_hour
