import json
import os

path = os.path.dirname(os.path.abspath(__file__))

with open(path + "/config/servers.json", "r", encoding="utf-8") as j:
    servers = json.load(j)

with open(path + "/config/item_names.json", "r", encoding="utf-8") as j:
    item_names = json.load(j)

for item_name in item_names:
    if "<" in item_name:
        item_name = item_name.replace("<", "(").replace(">", ")")
    if ":" in item_name:
        item_name = item_name.replace(":", "@")
    for server in servers:
        data_dir = path + "/data/" + server + "/" + item_name
        os.makedirs(data_dir)
        os.makedirs(data_dir + "/sale")
        os.makedirs(data_dir + "/history")
        os.makedirs(data_dir + "/sale/images")
        os.makedirs(data_dir + "/sale/data")
        os.makedirs(data_dir + "/history/images")
        os.makedirs(data_dir + "/history/data")
