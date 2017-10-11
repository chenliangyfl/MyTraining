#!/usr/bin/env python
#-*- coding: utf-8 -*-

from multiprocessing import Process, Queue
from Queue import Queue as _Que
# from threading import Thread
import gevent
from lxml import etree
import time
import requests


class DoubanSpider(Process):
    def __init__(self, url, q):
        super(DoubanSpider, self).__init__()
        self.url = url
        self.q = q
        self.header = {
            "Host": 'movie.douban.com',
            "Referer": 'https://movie.douban.com/top250?start=225&filter=',
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
        }
        self.header_fl = {
            "Host": 'www.dy2018.com',
            "Referer": 'http://www.dy2018.com/',
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
        }

    def run(self):
        self.parse_page()

    def send_request(self, url):
        for _ in range(3):
            try:
                print u"[INFO]请求url:{}".format(url)
                return requests.get(url=url, headers=self.header).content
            except Exception as e:
                print u"[ERROR]请求失败-->{}".format(e)

    def parse_page(self):
        resp = self.send_request(self.url)
        html = etree.HTML(resp)

        node_list = html.xpath("//div[@class='info']")
        for movie in node_list:
            movie_title = movie.xpath(".//a/span/text()")[0]
            movie_score = movie.xpath(".//div[@class='bd']//span[@class='rating_num']/text()")[0]
            self.q.put(movie_score + "\t" + movie_title)


def main():
    base_url = "https://movie.douban.com/top250?start="
    url_list = [base_url+str(num) for num in range(0, 226, 25)]

    q = Queue()
    pro_list = []
    for url in url_list:
        proc = DoubanSpider(url, q)
        proc.start()
        pro_list.append(proc)

    for p in pro_list:
        p.join()

    while not q.empty():
        print q.get()


class Dianshiju(object):
    def __init__(self):
        self.q = _Que()
        self.headers = {
            "Host": 'www.dy2018.com',
            "Referer": 'http://www.dy2018.com/',
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
        }

    def run(self, url):
        self.parse_page(url)

    def send_request(self, url):
        for _ in range(3):
            try:
                print u"[INFO]请求url:{}".format(url)
                return requests.get(url=url, headers=self.headers).content
            except Exception as e:
                print u"[ERROR]请求失败-->{}".format(e)

    def parse_page(self, url):
        resp = self.send_request(url)
        utf_resp = resp.decode('gbk', 'ignore')
        html = etree.HTML(utf_resp)

        node_list = html.xpath("//table[@style]")
        for a in node_list:
            ftp = a.xpath(".//a/text()")[0]
            self.q.put(ftp)

    def main(self, num):
        url = "http://www.dy2018.com/i/{}.html".format(num)

        self.run(url)

        while not self.q.empty():
            print self.q.get()


if __name__ == "__main__":
    start = time.time()

    # main()
    get_ftp = Dianshiju()

    get_ftp.main(98338)
    print u"[INFO]耗时:{}".format(time.time() - start)

