# -*- coding: utf-8 -*-
import scrapy


class TrainscheduleSpider(scrapy.Spider):
    name = 'TrainSchedule'
    start_urls = ['https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8C%97%E4%BA%AC,BJP&ts=%E7%9F%B3%E5%AE%B6%E5%BA%84,SJP&date=2018-12-09&flag=N,N,Y']

    def parse(self, response):
        #print(response)
        #with open('t.html', 'wb') as f:
         #   f.write(response.body)
        content=response.css("div.ticket-info.clearfix")
        for item in content:
            print(item.css("::text").extract())
