import requests
import re
from bs4 import BeautifulSoup

url='https://stackoverflow.com//'
filename='file_text.txt'

#zad1 pobrac strone
# response = requests.get(url).text
# file = open(filename, 'w+')
# file.write(response)
# file.close()

base='stackoverflow'
base_regex = r'http[s]*:\/\/stackoverflow'
is_link = 'http'
is_link_regex = r'http'
response = requests.get(url)
soup = BeautifulSoup(response.content)

stackoverflow_links = []
not_stackoverflow_links = []

unique_links = set(soup.find_all('a', href=True))
for link in unique_links:
    href = link['href']
    stackoverflow_link = True
    if re.match(base_regex, href):
        print(link['href'])
        print("stackowe!")
    elif re.match(is_link_regex, href):
        print(link['href'])
        print("NOT")
        stackoverflow_link = False
    if stackoverflow_link:
        stackoverflow_links.append(href)
    else:
        not_stackoverflow_links.append(href)

print(stackoverflow_links)
print(not_stackoverflow_links)
