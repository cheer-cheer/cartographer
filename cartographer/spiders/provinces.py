# -*- coding: utf-8 -*-
import scrapy
import errno
import datetime
import urllib.parse
from cartographer.items import *
import lxml.html
import re
from lxml.html.clean import Cleaner
from scrapy.exceptions import CloseSpider


class ProvincesSpider(scrapy.Spider):
    name = "provinces"
    allowed_domains = ["www.stats.gov.cn"]
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/']

    def parse(self, response):
        articles = response.css('.center .center_list_contlist li>a')

        items = []
        for article in articles:
            title = article.css('.cont_tit03::text').extract_first().strip()

            if not title.startswith('最新县及县以上行政区划代码（截止'):
                continue
            if not title.endswith('）'):
                continue

            due_date = datetime.datetime.strptime(title[16:-1], '%Y年%m月%d日')
            last_update = article.css('.cont_tit02::text').extract_first()
            last_update = datetime.datetime.strptime(last_update, '%Y-%m-%d')

            items.append({
                'title': title,
                'due_date': due_date,
                'last_update': last_update,
                'element': article
            })

        # for item in items:
        #     latest = item
        #     e = latest['element']
        #     article_url = e.css('::attr(href)').extract_first().strip()
        #     article_url = urllib.parse.urljoin(response.url, article_url)

        #     yield scrapy.Request(article_url, meta=latest,
        #                          callback=self.parse_article)

        items = sorted(items, key=lambda a: (a['due_date'], a['last_update']))

        latest = items[-1]
        e = latest['element']
        article_url = e.css('::attr(href)').extract_first().strip()
        article_url = urllib.parse.urljoin(response.url, article_url)

        yield scrapy.Request(article_url, meta=latest,
                             callback=self.parse_article)

    def parse_article(self, response):
        due_date = response.meta['due_date']
        last_update = response.meta['last_update']

        lines = response.css('.center .MsoNormal')

        pattern = re.compile(r'^(\d{6})\s*(\D+)$')
        html = response.css('.xilan_con').extract_first()
        cleaner = Cleaner(page_structure=False, style=True)
        html = cleaner.clean_html(html)
        html = lxml.html.fragment_fromstring(html)
        text = lxml.html.tostring(html, method='text', encoding='unicode')
        text = text.replace('代码', '', 1).replace('名称', '', 1)
        text = ''.join(text.split())
        parts = re.split(r'(\d{6})', text)
        # print('text:', parts[:30])
        i = 0
        count = len(parts)

        provinces = []
        province_count = 0
        city_count = 0
        district_count = 0
        while i < count:
            part = parts[i]
            if not part:
                i += 1
                continue

            if part.isdigit():
                code = part

                i += 1
                area = parts[i]

                if code.endswith('0000'):
                    a = Province(code=code, name=area)
                    provinces.append(a)
                    province_count += 1
                elif code.endswith('00'):
                    a = City(code=code, name=area)
                    province = provinces[-1]
                    cities = province.get('cities') or []
                    cities.append(a)
                    province['cities'] = cities
                    city_count += 1
                else:
                    a = District(code=code, name=area)

                    city = provinces[-1]['cities'][-1]
                    districts = city.get('districts') or []
                    districts.append(a)
                    city['districts'] = districts
                    district_count += 1
            else:
                raise CloseSpider('行政区划代码无效: %s' % (part, ))

            i += 1

        print('(更新于 %s) 截止至 %s 县及县以上行政区划代码: \
采集到省份 %d 个，城市 %d 个，区县 %d 个' %
              (last_update.strftime('%Y-%m-%d'), due_date.strftime('%Y-%m-%d'),
               province_count, city_count, district_count))

        yield Areas(due_date=due_date, last_update=last_update,
                    provinces=provinces)
