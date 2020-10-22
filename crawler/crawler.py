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
item_states = ["sale", "history"]
item_states_id = {
    "sale": "auction-list",
    "history": "auction-history"
}

# data format
columns = ["price", "option", "additional", "star_force", "upgrade", "time_remained", "item_code"]

def item_parser(item, is_additional_option):      
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


def main(item_info):
    server, item_name = item_info[0], item_info[1]
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
        root_data_dir = "{}/data/{}/{}/{}".format(path, server, item_name, item_state)
        img_dir = "{}/images/{}".format(root_data_dir, timestamp)
        os.mkdir(img_dir)

        div = soup.find(id=item_states_id[item_state])
        table = div.find('table')
        table_head = table.select('thead')[0]
        table_body = table.select('tbody')[0]
        items = table_body.find_all("tr")

        is_additional_option = (table_head.find_all("th")[2].text == "추옵")

        result_data = []

        for item_code, item in enumerate(items[:2]):        ###############################
            data = item_parser(item, is_additional_option)
            data.append(item_code) 
            result_data.append(data)
            
            img = item_image_parser(item)
            img.save("{}/{}.png".format(img_dir, item_code))

        with open("{}/data/{}.csv".format(root_data_dir, timestamp), "w", encoding="utf-8") as c:
            c.write(",".join(columns))
            c.write("\n")
            for d in result_data:
                c.write(",".join(map(str, d)))
                c.write("\n")

if __name__ == "__main__":
    server = "스카니아"
    #item_name = "앱솔랩스 스펠링완드"
    item_name = "아케인셰이드 가즈"

    main((item_name, server))