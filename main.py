import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
response = requests.get('https://app.hwestauctions.com')
if response.status_code != 200:
    print("error")

soup = BeautifulSoup(response.text, 'html.parser')
l = soup.select_one('.accordion')
data = {}
for val in list(filter(lambda a: a!='\n', l.contents[1:])):
    try:
        val_data = []
        for auction in val.select('.card'):
            bid = auction.select_one('li').get_text()
            val_data.append(
                {
                    'address':auction.select_one('.card-title').get_text(),
                    'info':auction.select_one('.card-text').get_text(),
                    'bid': bid[13:len(bid)]
                }
            )
        title = val.contents[1].get_text().strip()
        data[title[12:len(title)] if title[0]!='T' else 'Today'] = val_data
    except Exception as e:
        print(e)
with open('out.json','w') as file:
    file.write(json.dumps(data,indent=4, sort_keys=True))
