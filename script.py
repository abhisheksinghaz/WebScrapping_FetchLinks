import requests
from bs4 import BeautifulSoup

url = "<the link goes here>"

r = requests.get(url)
htmlContent = r.content

soup = BeautifulSoup(htmlContent, 'html.parser')
anchors = soup.find_all('a')

for link in anchors:
  print(link['href'])
