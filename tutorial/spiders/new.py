# -*- coding: utf-8 -*-

import scrapy
from tutorial.items import DmozItem
import time

class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["zhaiiker.com"]
    #start_urls = [
    #    "https://www.zhaiiker.com/category/resource/4kresource"
    #]

    def start_requests(self):
        url = 'https://www.zhaiiker.com/category/resource/4kresource'
        # FormRequest 是Scrapy发送POST请求的方法
        for i in range(1,100):
            yield scrapy.FormRequest(
                url=url,
                formdata={"paged": str(i), "append": "d-archive", "action": "ajax_load_posts", "query":"416", "page":"cat"},
                callback=self.parse
            )
            #time.sleep(1)





    def parse(self, response):
        moviename = response.xpath('//h2/a')
        for i in moviename:
            item = DmozItem()
            item['name'] = i.xpath('text()').extract()
            item['link'] = i.xpath('@href').extract()
            yield item
