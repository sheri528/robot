# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import unicode_literals
import time

from scrapy.mail import MailSender
from scrapy import signals
from scrapy.exporters import XmlItemExporter, CsvItemExporter

class XmlExportPipeline(object):

    def __init__(self):
        self.files = {}

    def open_spider(self, spider):
        file = open('%s_products.xml' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = XmlItemExporter(file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class CsvExportPipeline(XmlExportPipeline):

    def __init__(self):
        self.files = {}

    def open_spider(self, spider):
        file = open('%s_products.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.start_exporting()


class GrabSendingEmailPipeline(object):
    ''' Base class for sending E-mail. '''
    mailer = MailSender(smtphost='smtp.exmail.qq.com',
                        mailfrom='mail@xxx',
                        smtpuser='user@xxx',
                        smtppass='password')

    def close_spider(self, spider):
        pass

class EbaySendingEmailPipeline(GrabSendingEmailPipeline):

    def __init__(self, *args, **kwargs):
        super(EbaySendingEmailPipeline, self).__init__(*args, **kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_closed(self, spider):
        ''' To: xxmail
            Cc :xxmail '''

        attach_name = "ebay_data_{}.xml".format(time.strftime('%y%m%d', time.localtime(time.time())))
        mimetype = 'application/octet-stream'
        file_object = open('%s_products.xml' % spider.name, 'r')

        self.mailer.send(
            to=["xx@qq.com", ],
            cc=["xx@qq.com"],
            subject="search xx in ebay",
            body="Hi~, \n\n Here is all items in ebay when searching for 'xxx'.\
            \n\n Attachs could use Excel to open.\
            \n\n If there's any question, Please contact me.\
            \n\n Best regards\
            \n user@qq.com",
            attachs=((attach_name, mimetype, file_object),),
            charset='utf8'
        )
