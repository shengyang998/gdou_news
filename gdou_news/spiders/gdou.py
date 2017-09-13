# -*- coding: utf-8 -*-
import scrapy
from collections import deque
import re
import urllib

class GdouSpider(scrapy.Spider):
    name = 'gdou'
    allowed_domains = ['news.gdou.edu.cn']
    news_url_prefix = "http://news.gdou.edu.cn/show.php?contentid="
    url_list = deque()
    for i in range(454, 22941):
    # for i in range(454, 535):
        url_list.append(news_url_prefix + str(i+1))
    start_urls = list(url_list)

    def parse(self, response):
        # print("Response: {0}".format(response.xpath('//h1/text()')))
        # print("Title: {0}\nTime: {1}\nDesc: {2}\nBody: {3}\nImg Url: {4}".format(title, time, desc, body, img_url))
        url = response.url
        # print(url)
        title = [ x.strip() for x in response.xpath('//h1//text()').extract() if x.strip() != "" ]
        time = [ x.strip() for x in response.xpath('//h2/span/text()').extract() if x.strip() != "" and x.strip() != "0" ]
        author_audit = [ x.strip() for x in response.xpath('//h2//text()').re(r'作者：(.*)来源') if x.strip() != "" ]
        origin = [ x.strip() for x in response.xpath('//h2//text()').re(r'来源：(.*)浏览') if x.strip() != "" ]
        body = [ x.strip() for x in response.xpath('//div[@id="endtext"]//text()').extract() if x.strip() != "" ]
        imgs_url = [ x.strip() for x in response.xpath('//div[@id="endtext"]//img/@src').extract() if x.strip() != "" ]
        keywords = [ x.strip() for x in response.xpath('//div[@id="keyword"]/a[@class="keyword"]/text()').extract() if x.strip() != "" ]
        if time != []:
            yield {
                'url': url,
                'title': title,
                'time': time,
                'author': author_audit,
                'origin': origin,
                'body': body,
                'imgs_url': imgs_url,
                'keywords': keywords
            }

