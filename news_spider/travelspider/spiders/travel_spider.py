# coding=utf-8
import scrapy
from urllib import request
import pymongo
from lxml import etree
from travelspider.items import TravelspiderItem

class TravelSpider(scrapy.Spider):
    name = 'travel'
    '''资讯采集主控函数'''
    def start_requests(self):
        for index in range(1, 650001):
            url = 'http://www.5nd.com/ting/%s.html'%index
            try:
                print(url)
                param = {'url': url}
                yield scrapy.Request(url=url, meta=param, callback=self.page_parser, dont_filter=True)
            except:
                pass

    '''网页解析'''
    def page_parser(self, response):
        content = response.text
        content = content.replace('<br>', '\n').replace('<br />', '\n')
        selector = etree.HTML(content)
        song = selector.xpath('//h1/a/text()')[0]
        singer = selector.xpath('//li/a[@target="_singer"]/text()')[0]
        album = selector.xpath('//li/a[@target="_album"]/text()')[0]
        geci = selector.xpath('//div[@class="songLyricCon"]/p/text()')[0]
        item = TravelspiderItem()
        item['url'] = response.meta['url']
        item['singer'] = singer
        item['song'] = song
        item['geci'] = geci
        item['album'] = album
        yield item
        return
