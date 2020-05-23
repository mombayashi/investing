# -*- coding: utf-8 -*-
import scrapy
from investing.items import StockItem

class InvestingSpider(scrapy.Spider):
    name = 'investing'
    allowed_domains = ['jp.investing.com']
    start_urls = ['https://jp.investing.com/equities/softbank-corp.-historical-data']

    def parse(self, response):
        prices = response.xpath('//*[@id="results_box"]/table/tbody/tr')
        for price in prices[:-1]:
            item = StockItem()
            item['stock_date'] = price.xpath('td[1]//text()').extract_first()
            item['stock_end'] = price.xpath('td[2]//text()').extract_first()
            item['stock_begin'] = price.xpath('td[3]//text()').extract_first()
            item['stock_high'] = price.xpath('td[4]//text()').extract_first()
            item['stock_low'] = price.xpath('td[5]//text()').extract_first()
            item['stock_vol'] = price.xpath('td[6]//text()').extract_first()
            item['stock_ratio'] = price.xpath('td[7]//text()').extract_first()
            yield item

