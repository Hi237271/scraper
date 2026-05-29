import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


def getZestimate(address):
    try:
        response = requests.get('https://zillow.realtyapi.io/pro/byaddress', headers={
            "x-realtyapi-key": "rt_W5n7GCcI1XmUtdKOP7bvdOuH"
        }, params={"propertyaddress": address})
        data = response.json()
    except:
        return 'null'
    return data['propertyDetails']['zestimate']


def getChildren(l):
    return list(filter(lambda a: a != '\n', l.contents))


response = requests.get('https://app.hwestauctions.com')
if response.status_code != 200:
    print("error")

soup = BeautifulSoup(response.text, 'html.parser')
l = soup.select_one('.accordion')
data = []
for val in list(filter(lambda a: a != '\n', l.contents[1:])):
    try:
        val_data = []
        for auction in val.select('.card'):
            bid = auction.select_one('li').get_text()
            title = val.contents[1].get_text().strip()
            info = auction.select_one('.card-text').get_text()
            time = ''
            try:
                time = info[32:31 + info[32:].index('at')]
            except Exception as e:
                time = 'null'
                print(f"INFO: {info}")
                print('exception. error: ', e)
            data.append(
                {
                    'date': title[12:len(title)] if title[0] != 'T' else 'Today',
                    'time': time,
                    'address': auction.select_one('.card-title').get_text(),
                    'deposit': bid[13:len(bid)],
                    'zestimate': getZestimate(auction.select_one('.card-title').get_text())
                }
            )
        title = val.contents[1].get_text().strip()
    except Exception as e:
        print(e)
with open('out.json', 'w') as file:
    file.write(json.dumps(data, indent=4, sort_keys=True))
response = requests.get(
    'https://www.tidewaterauctions.com/upcoming-real-estate-auctions')
if response.status_code != 200:
    print("error")

soup = BeautifulSoup(response.text, 'html.parser')
l = soup.select('.us-block')
for a in l:
    k = getChildren(a)[1]
    element_data = []
    for elt in getChildren(k)[1:]:
        vals = list(filter(lambda a: len(a.get_text().strip())
                    > 0, elt.select('span,a')))
        try:
            element_data.append(
                {
                    "time": vals[0].get_text(),
                    "address": vals[1].get_text(),
                    "deposit": vals[2].get_text(),
                    "client": vals[3].get_text()
                }
            )
            data.append(
                {
                    "date": getChildren(a)[0].select_one('span').get_text(),
                    "time": vals[0].get_text(),
                    "address": vals[1].get_text(),
                    "deposit": vals[2].get_text(),
                    'zestimate': getZestimate(auction.select_one('.card-title').get_text())
                }
            )
        except Exception as e:
            pass
            # print("Error: ",e)
            # print("Occured for element: ",elt)
df = pd.read_json(json.dumps(data, indent=4))
df.to_csv("auctions.csv", encoding='utf-8')
df.to_excel('auctions.xlsx')
