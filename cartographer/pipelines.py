# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from scrapy.utils.serialize import ScrapyJSONEncoder
import os


class ProvincesPipeline(object):

    def process_item(self, item, spider):
        due_date = item['due_date']
        last_update = item['last_update']

        data_file_name = './data/' + due_date.strftime('%y%m%d') + '_' + \
            last_update.strftime('%y%m%d') + '.json'

        os.makedirs(os.path.dirname(data_file_name), exist_ok=True)

        with open(data_file_name, 'w+') as f:
            f.write(ScrapyJSONEncoder().encode(item['provinces']))

        print('已保存到数据文件:', data_file_name)
        return item
