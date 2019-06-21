#!/usr/bin/env python
import urllib2
from bs4 import BeautifulSoup
import json
import pika
from pika.exceptions import AMQPConnectionError

import time
from threading import Thread, Timer
import random
import re

from pymongo import MongoClient


class ScrapedPost:
    def __init__(self, title, url, createdDatetime, site, keyword, description):
        self.title = title
        self.url = url
        self.createdDatetime = createdDatetime
        self.site = site
        self.keyword = keyword
        self.description = description


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
NOTIFICATIONS_COLLECTION = 'notifications'

WYKOP_SCRAPING_INTERVAL = 15    #seconds

debug = False
logInfo = True

dbClient = 'global'
collSubscribedWords = 'global'
collScrapedPosts = 'global'
collNotifications = 'global'

subscribedWordsDict = {}
rabbitMQConn = 'global'


zmienna = 1


def initDatabaseConnection():
    global dbClient, collScrapedPosts, collSubscribedWords
    dbClient = MongoClient('mongodb://root:root@localhost:27017')
    collSubscribedWords = dbClient[DATABASE_NAME][SUBSCRIBED_WORDS_COLLECTION]
    collScrapedPosts = dbClient[DATABASE_NAME][SCRAPED_POSTS_COLLECTION]
    collNotifications = dbClient[DATABASE_NAME][NOTIFICATIONS_COLLECTION]


def initDatabaseData():
    for subscribedWord in collSubscribedWords.find():
        subscribeIfUniqe(subscribedWord['keyword'], subscribedWord['username'])


def startWebScraper(interval, webscraperCallback):
    oldInterval = interval
    if RANDOMIZE_BEHAVIOR:
        interval += random.randint(0, 4)
    Timer(interval, startWebScraper, [oldInterval, webscraperCallback]).start()
    webscraperCallback()


def getHtmlFromSite(url):
    global AGENTS
    request = urllib2.build_opener()
    if RANDOMIZE_BEHAVIOR:
        request.addheaders = [('User-Agent', random.choice(AGENTS))]
    return request.open(url).read()


def scrapWykop():
    global subscribedWordsDict, logInfo
    if logInfo:
        print("\nStarted scrap wykop.pl")
        print("Words set: " + str(subscribedWordsDict) + "\n")
    for keyword, user in subscribedWordsDict.iteritems():
        print("Searching for keyword = " + keyword)
        url = 'https://www.wykop.pl/szukaj/' + keyword + '/?search%5Bsort%5D=new'
        html = getHtmlFromSite(url)
        saveWykopElements(html, keyword)


def saveWykopElements(html, keyword):
    global debug, logInfo
    soup = BeautifulSoup(html, 'html.parser')
    for li in soup.find(id='itemsStream').find_all('li'):
        wykopPostDiv = li.find('div').find('div', {'class': 'lcontrast'})
        wykopPostLink = wykopPostDiv.h2.a
        wykopPostDescription = wykopPostDiv.find('div', {'class': 'description'}).p.a.text
        wykopPostDescription = wykopPostDescription.replace('\n', '').replace('\t', '')     #remove \n \t from text
        datetime = wykopPostDiv.select('div.row.elements')[0].span.time['datetime']
        scrapedPost = ScrapedPost(wykopPostLink['title'], wykopPostLink['href'], datetime, 'wykop', keyword, wykopPostDescription)
        addPostIfNotExists(scrapedPost, keyword)

        if debug:
            print(scrapedPost.title)
            print(scrapedPost.url)
            print(scrapedPost.createdDatetime)
            print("\n")

def addPostIfNotExists(scrapedPost, keyword):
    global logInfo
    existingPost = collScrapedPosts.find_one(scrapedPost.__dict__)
    if not existingPost:
        createNotifications(keyword)
        collScrapedPosts.insert(scrapedPost.__dict__)
        if logInfo:
            print("\tNew post: " + scrapedPost.title + " ( DATETIME: " + scrapedPost.createdDatetime + ")")

def createNotifications(keyword):
    global rabbitMQConn
    channel = rabbitMQConn.channel()
    for subscribedWord, users in subscribedWordsDict.iteritems():
        if subscribedWord == keyword:
            for user in users:
                body = {'username': user, 'keyword': subscribedWord}
                channel.basic_publish(exchange='', routing_key='notification', body=json.dumps(body))
    channel.close()


def subscribeIfUniqe(keyword, username):
    #insert to dict var from another thread - may cause exceptions
    global subscribedWordsDict, logInfo
    usernames = subscribedWordsDict.get(keyword)
    if usernames is None:
        subscribedWordsDict[keyword] = [username]
        if logInfo:
            print("Subscribed user = " + username + " for keyword = " + keyword)
    elif username not in usernames:
        subscribedWordsDict[keyword].append(username)
        if logInfo:
            print("Subscribed user = " + username + " for keyword = " + keyword)
    else:
        if logInfo:
            print("User = " + username + " has already subscribed keyword = " + keyword)


def subscribeCallback(ch, method, properties, body):
    global logInfo
    if logInfo:
        print("Received from rabbitQM: " + body)
    bodyDict = json.loads(body)
    keyword = bodyDict["keyword"]
    username = bodyDict["username"]
    subscribeIfUniqe(keyword, username)


def startListeningToSubscriptions(connection):
    channel = connection.channel()
    channel.basic_consume(queue=SUBSCRIPTION_QUEUE_NAME, auto_ack=True, on_message_callback=subscribeCallback)

    print('\n[*] RabbitMQ - listening queue "subscription" Waiting for messages. To exit press CTRL+C')
    print("\n")
    channel.start_consuming()


# main:
initDatabaseConnection()
initDatabaseData()

try:
    rabbitMQConn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    startWebScraper(WYKOP_SCRAPING_INTERVAL, scrapWykop)

    startListeningToSubscriptions(rabbitMQConn)
except AMQPConnectionError:
    print(' RabbitMQ connection problem')
