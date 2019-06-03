import urllib.request
import nltk
from nltk.corpus import stopwords
import requests

from bs4.element import Comment
from bs4 import BeautifulSoup

url='https://stackoverflow.com//'
filename='file_text.txt'

# response = requests.get(url)
#
# soup = BeautifulSoup(response.content, 'html.parser')
#
# print(soup['body'])
stpwords = set(stopwords.words('english'))

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    all = u" ".join(t.strip() for t in visible_texts)
    return [word for word in all.split() if not word in stpwords]

html = urllib.request.urlopen(url).read()
text = text_from_html(html)
for word in set(text):
    print(word)