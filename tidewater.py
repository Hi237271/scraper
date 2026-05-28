import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
def getChildren(l):
    return list(filter(lambda a: a!='\n', l.contents))
response = requests.get('https://www.tidewaterauctions.com/upcoming-real-estate-auctions')
if response.status_code != 200:
    print("error")

soup = BeautifulSoup(response.text, 'html.parser')
l = soup.select('.us-block')
data = []
csv_data = []
for a in l:
    k = getChildren(a)[1]
    element_data = []
    for elt in getChildren(k)[1:]:
        vals = list(filter(lambda a : len(a.get_text().strip())>0, elt.select('span,a')))
        try:
            element_data.append(
                {
                    "time":vals[0].get_text(),
                    "address":vals[1].get_text(),
                    "deposit":vals[2].get_text(),
                    "client":vals[3].get_text()
                }
            )
            csv_data.append(
                {
                    "date":getChildren(a)[0].select_one('span').get_text(),
                    "location":getChildren(a)[0].select('span')[-1].get_text(),
                    "time":vals[0].get_text(),
                    "address":vals[1].get_text(),
                    "deposit":vals[2].get_text(),
                    "client":vals[3].get_text()           
                }
            )
        except Exception as e:
            pass
            # print("Error: ",e)
            # print("Occured for element: ",elt)
    data.append(
        {
            "date":getChildren(a)[0].select_one('span').get_text(),
            "location":getChildren(a)[0].select('span')[-1].get_text(),
            "auctions":element_data
        }
    )
print(json.dumps(data,indent=4))
with open("tidewater.csv",'w') as file:
    df = pd.read_json(json.dumps(csv_data,indent=4))
    df.to_csv("tidewater.csv",encoding='utf-8')
    df.to_excel('tidewater.xlsx')