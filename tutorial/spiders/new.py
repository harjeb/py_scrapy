# -*- coding: utf-8 -*-

import scrapy
from tutorial.items import DmozItem
import time,re

class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["zhaiiker.com"]
    #start_urls = [
    #    "https://www.zhaiiker.com/category/resource/4kresource"
    #]


    def start_requests(self):
        url = 'https://www.zhaiiker.com/category/resource/4kresource'
        # FormRequest 是Scrapy发送POST请求的方法
        for i in range(1,2):   #抓取前30页数据
            yield scrapy.FormRequest(
                url=url,
                formdata={"paged": str(i), "append": "d-archive", "action": "ajax_load_posts", "query":"416", "page":"cat"},
                callback=self.parse
            )
            #time.sleep(1)


    def parse(self, response):
        if response.status == 200:
            moviename = response.xpath('//h2/a')
            for i in moviename:
                item = DmozItem()
                item['name'] = i.xpath('text()').extract()
                item['link'] = i.xpath('@href').extract()
                url = ''.join(item['link'])
                yield scrapy.Request(url,meta={'item':item}, callback=self.parse_dir_contents)


    def parse_dir_contents(self, response):
        imagexpath = response.xpath('//article/div[@class="post-image"]/img[contains(@class,"size-full")]')
        downloadurls = response.xpath('//a[@rel="noopener"]')
        item = response.meta['item']
        item['image_urls'] = imagexpath.xpath('@src').extract()
        item['downloadlink'] = downloadurls.xpath('@href').extract()
        yield item

