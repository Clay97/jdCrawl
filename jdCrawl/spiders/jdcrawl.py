# -*- coding: utf-8 -*-
import scrapy
from jdCrawl.items import JdcrawlItem
class JdcrawlSpider(scrapy.Spider):
    name = 'jdcrawl'
    allowed_domains = ['search.jd.com']
    base_url ='https://search.jd.com/Search?enc=utf-8&keyword='

    global a
    def start_requests(self):
        for key in self.settings.get('KEYWORDS'):
            for page in range(1,self.settings.get('MAX_PAGE')+1):
                url = self.base_url+key
                yield scrapy.Request(url=url, meta={'page': page}, callback=self.parse, dont_filter=True)

    def parse(self, response):
        products= response.xpath("//li[@class='gl-item']").extract()
        print('-'*50)
        #print(products)
        a=1
        for product in products:
            print(a)
            a+=1
            item = JdcrawlItem()
            productitem = scrapy.Selector(text=product)
            item['price'] = productitem.xpath(".//div/div[3]/strong/i/text()").extract()[-1]
            item['title'] = productitem.xpath(".//div/div[4]/a/em/text()").extract()[-1]
            item['comment'] = productitem.xpath(".//div/div[5]/strong/a/text()").extract()[-1]
            item['shop'] = productitem.xpath(".//div/div[7]/span/a/text()").extract()[-1]
            item['icons'] = productitem.xpath(".//div/div[8]/i/text()").extract()
            yield item

