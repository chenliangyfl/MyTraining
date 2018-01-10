#!/usr/bin/env python
#-*- coding: utf-8 -*-
import pika

# credentials = pika.PlainCredentials("chenliang", "860214qq")
# connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1",
#                                                                5672, '/',
#                                                                credentials))
connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1"))
channel = connection.channel()
channel.queue_declare(queue="clqueue", durable=True)

channel.basic_publish(exchange='', routing_key="clqueue",
                      body="hello rabbitmq!!",
                      properties=pika.BasicProperties(delivery_mode=2))

print "[x] sent hello rabbitmq."
connection.close()
