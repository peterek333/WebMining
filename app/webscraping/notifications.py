#!/usr/bin/env python
import urllib2
from bs4 import BeautifulSoup
import json
import pika
from pika.exceptions import AMQPConnectionError

import time
from threading import Thread, Timer
import random

from pymongo import MongoClient


class ScrapedPost:
    def __init__(self, title, url, createdDatetime):
        self.title = title
        self.url = url
        self.createdDatetime = createdDatetime


RANDOMIZE_BEHAVIOR = True
AGENTS = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
]

SUBSCRIPTION_QUEUE_NAME = 'subscription'
DATABASE_NAME = 'scraped'
SUBSCRIBED_WORDS_COLLECTION = 'subscribedWord'
SCRAPED_POSTS_COLLECTION = 'scrapedPost'

dbClient = 'global'
collSubscribedWords = 'global'
collScrapedPosts = 'global'

subscribedWordsDict = {}


zmienna = 1


def initDatabaseConnection():
    global dbClient, collScrapedPosts, collSubscribedWords
    dbClient = MongoClient('mongodb://root:root@localhost:27017')
    collSubscribedWords = dbClient[DATABASE_NAME][SUBSCRIBED_WORDS_COLLECTION]
    collScrapedPosts = dbClient[DATABASE_NAME][SCRAPED_POSTS_COLLECTION]


def startWebScraper(interval, webscraperCallback):
    if RANDOMIZE_BEHAVIOR:
        interval += random.randint(0, 4)
    Timer(interval, startWebScraper, [interval, webscraperCallback]).start()
    webscraperCallback()


def getHtmlFromSite(url):
    global AGENTS
    request = urllib2.build_opener()
    if RANDOMIZE_BEHAVIOR:
        request.addheaders = [('User-Agent', random.choice(AGENTS))]
    return request.open(url).read()


def scrapWykop():
    # url = 'https://www.wykop.pl/szukaj'
    url = 'https://www.wykop.pl/szukaj/czolg/'
    html = getHtmlFromSite(url)
    getWykopElements(html)


def getWykopElements(html):
    soup = BeautifulSoup(html, 'html.parser')
    for li in soup.find(id='itemsStream').find_all('li'):
        wykopPostDiv = li.find('div').find('div', {'class': 'lcontrast'})
        wykopPostLink = wykopPostDiv.h2.a
        datetime = wykopPostDiv.select('div.row.elements')[0].span.time['datetime']
        scrapedPost = ScrapedPost(wykopPostLink['title'], wykopPostLink['href'], datetime)

        print(scrapedPost.title)
        print(scrapedPost.url)
        print(scrapedPost.createdDatetime)
        print("\n\n")


def subscribeIfUniqe(keyword, username):
    global subscribedWordsDict
    usernames = subscribedWordsDict.get(keyword)
    if usernames is None:
        subscribedWordsDict[keyword] = [username]
    elif username not in usernames:
        subscribedWordsDict[keyword].append(username)


def subscribeCallback(ch, method, properties, body):
    print("Received " + body)
    bodyDict = json.loads(body)
    # print(bodyDict)
    # print(type(bodyDict))
    # print(bodyDict["keyword"])
    # print(bodyDict["username"])
    keyword = bodyDict["keyword"]
    username = bodyDict["username"]
    subscribeIfUniqe(keyword, username)


def startListeningToSubscriptions(connection):
    channel = connection.channel()
    channel.basic_consume(queue=SUBSCRIPTION_QUEUE_NAME, auto_ack=True, on_message_callback=subscribeCallback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def mockSubscribedData():
    subscribeCallback('', '', '', json.dumps({
        'keyword': 'word', 'username': 'user1'
    }))
    subscribeCallback('', '', '', json.dumps({
        'keyword': 'word', 'username': 'user2'
    }))
    subscribeCallback('', '', '', json.dumps({
        'keyword': 'word', 'username': 'user1'
    }))
    subscribeCallback('', '', '', json.dumps({
        'keyword': 'word2', 'username': 'user1'
    }))
    subscribeCallback('', '', '', json.dumps({
        'keyword': 'word2', 'username': 'user1'
    }))
    for k, v in subscribedWordsDict.iteritems():
        print(k, v)


def initDatabaseData():
    for subscribedWord in collSubscribedWords.find():
        subscribeIfUniqe(subscribedWord['keyword'], subscribedWord['username'])


# main:
mockSubscribedData()
initDatabaseConnection()
initDatabaseData()

scrapWykop()
# startWebScraper(4, threadtest)

try:
    rabbitMQConn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    startListeningToSubscriptions(rabbitMQConn)
except AMQPConnectionError:
    print(' RabbitMQ connection problem')




# thread = Thread(target=threadtest)
# thread.start()
# thread.join()

