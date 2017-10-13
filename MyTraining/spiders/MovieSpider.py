#!/usr/bin/env python
#-*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from MyTraining.items import MytrainingItem


class MovieSpider(BaseSpider):
    name = "moviesp"
    allowed_domains = ["dy2018.com"]
    start_urls = ["http://www.dy2018.com/html/tv/hytv/index.html"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.xpath("//table[@style]//a")

        items = []
        for site in sites:
            item = MytrainingItem()
            item['title'] = ''.join(site.xpath("@title").extract())
            item['link'] = site.xpath("@href").extract()
            item['desc'] = ''.join(site.xpath("text()").extract())
            items.append(item)
        return items
