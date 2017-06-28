# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Areas(scrapy.Item):
    provinces = scrapy.Field()
    last_update = scrapy.Field()
    due_date = scrapy.Field()


class Province(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    cities = scrapy.Field()


class City(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    districts = scrapy.Field()


class District(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
