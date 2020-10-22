import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import datetime
import json
import re
import os

path = os.path.dirname(os.path.abspath(__file__))

# requests 
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
base_url = "https://maple.market/items"

# configs
with open(path + "/config/servers.json", "r", encoding="utf-8") as j:
    servers = json.load(j)

with open(path + "/config/item_names.json", "r", encoding="utf-8") as j:
    item_names = json.load(j)

item_states = ["sale", "history"]
item_states_id = {
    "sale": "auction-list",
    "history": "auction-history"
}

# data format
columns = ["price", "option", "additional", "star_force", "upgrade", "time_remained"]

def item_parser(item, is_additional_option=False):      
    # additional_option == 추옵 (무기류)
    if is_additional_option:
        mapping = [1, 3, 4, 5, 7]
    else:
        mapping = [1, 2, 3, 4, 6]

    data = []
    item_contents = item.find_all("td")
    
    # 1, 2
    item_name_span = item_contents[mapping[0]].select("span")[0]
    star_force = 0
    upgrade = 0
    item_name_raw = item_name_span.text.strip()

    if item_name_span.find("div") != None:
        star_force = int(item_name_raw[-1])
        item_name_raw = item_name_raw[:-1].strip()

    m = re.compile("\+(\d*)")

    if m.search(item_name_raw) != None:
        upgrade = int(m.search(item_name_raw).group(1))

    # 3
    option = item_contents[mapping[1]].text.strip()

    # 4
    additional = item_contents[mapping[2]].text.strip()

    # 5 
    price = int(item_contents[mapping[3]].text.strip().split("\n")[0].replace(',',''))

    # 6
    time_remained = item_contents[mapping[4]].text.strip()

    data.append(price)
    data.append(option)
    data.append(additional)
    data.append(star_force)
    data.append(upgrade)
    data.append(time_remained)

    return data

def item_image_parser(item):
    item_image_url = item.find_all("td")[1].select("div")[0].attrs["data-tooltip-image-url"]
    item_image_content = requests.get(item_image_url, headers=headers)
    assert(item_image_content.status_code == 200)

    stream = io.BytesIO(item_image_content.content)
    item_image = Image.open(stream)

    return item_image

# Roop
server = servers[3]
j = 50
item_name = item_names[j]

if j < 95:
    is_additional_option = True
else:
    is_additional_option = False

timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

url = "{}/{}/{}".format(base_url, item_name.replace(" ", ""), server)

req = requests.get(url, headers=headers)
html = req.text
soup = BeautifulSoup(html, 'lxml')

if "<" in item_name:
    item_name = item_name.replace("<", "(").replace(">", ")")
if ":" in item_name:
    item_name = item_name.replace(":", "@")

for item_state in item_states:
    data_dir = path + "/data/" + server + "/" + item_name + "/" + item_state

    div = soup.find(id=item_states_id[item_state])
    table = div.find('table')
    table_head = table.select('thead')[0]
    table_body = table.select('tbody')[0]
    items = table_body.find_all("tr")

    result_data = []
    result_images = []

    for item in items:
        d = item_parser(item, is_additional_option=is_additional_option)
        result_data.append(d)
        #img = item_image_parser(item)
        #result_images.append(img)

    #assert(len(result_data) == len(result_images))

    print(result_data)
    print(item_name)

    with open("{}/data/{}.csv".format(data_dir, timestamp), "w", encoding="utf-8") as c:
        c.write(",".join(columns))
        c.write("\n")
        for d in result_data:
            c.write(",".join(map(str, d)))
            c.write("\n")