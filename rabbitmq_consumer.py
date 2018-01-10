#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pika

credentials = pika.PlainCredentials("admin", "admin")
connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1",
                                                              5672, '/',
                                                              credentials))
# connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1"))
channel = connection.channel()
channel.queue_declare(queue="clqueue", durable=True)


def callback(ch, method, proper, body):
    print "[x] received {}".format(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(callback, queue="clqueue")

print '[*] Waiting for message.To exix preee CTRL+C'

channel.start_consuming()