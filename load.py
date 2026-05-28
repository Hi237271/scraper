import requests
from bs4 import BeautifulSoup


url = 'https://app.hwestauctions.com'

response = requests.get(url)

if response.status_code != 200:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')
l = soup.select_one('.accordion')