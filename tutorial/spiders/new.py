# -*- coding: utf-8 -*-

import scrapy
from tutorial.items import DmozItem

class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["zhaiiker.com"]
    start_urls = [
        "https://www.zhaiiker.com/category/resource/4kresource"
    ]

    def parse(self, response):
        moviename = response.xpath('//h2/a')
        for i in moviename:
            item = DmozItem()
            item['name'] = i.xpath('text()').extract()
            item['link'] = i.xpath('@href').extract()
            yield item
