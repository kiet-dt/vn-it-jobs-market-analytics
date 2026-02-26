# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from kafka import KafkaProducer
import json

class KafkaPipeline:
    def open_spider(self, spider):
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def process_item(self, item, spider):
        self.producer.send(
            topic='itviec',
            value=dict(item)
        )
        return item

    def close_spider(self,spider):
        self.producer.flush()
        self.producer.close()