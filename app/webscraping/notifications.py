#!/usr/bin/env python
import pika
import json

import time
from threading import Thread


def subscribeCallback(ch, method, properties, body):
    print("Received " + body)
    obj = json.loads(body)
    print(obj)
    print(type(obj))
    print(obj["keyword"])
    print(obj["username"])


def threadtest():
    time.sleep(3)
    print("dziala")


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.basic_consume(queue='subscription', auto_ack=True, on_message_callback=subscribeCallback)

thread = Thread(target=threadtest)
thread.start()
# thread.join()

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
