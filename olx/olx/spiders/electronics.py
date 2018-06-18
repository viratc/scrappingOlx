# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from olx.items import OlxItem

class ElectronicsSpider(CrawlSpider):
    name = 'electronics'
    allowed_domains = ['www.olx.in']
    start_urls = ['https://www.olx.in/computer-accessories/',
    'https://www.olx.in/tv-video-audio/',
    'https://www.olx.in/games-entertainment/']

    rules = (
    	Rule(LinkExtractor(allow=(), restrict_css=('.pageNextPrev',)),
    	                        callback="parse_item",follow=True),)

    def parse_item(self, response):
    	item_links = response.css('.large > .detailsLink::attr(href)').extract()
    	for a in item_links:
    		yield scrapy.Request(a, callback = self.parse_detail_page) 

    def parse_detail_page(self, response):
    	title = response.css('h1::text').extract()[0].strip()
    	price = response.css('.pricelabel > strong::text').extract()[0]

    	item = OlxItem()
    	item['title'] = title
    	item['price'] = price
    	item['url'] = response.url
    	yield item

