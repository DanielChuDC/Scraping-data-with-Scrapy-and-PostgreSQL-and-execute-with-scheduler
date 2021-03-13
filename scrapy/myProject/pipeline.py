
from scrapy import signals
from scrapy.exporters import CsvItemExporter

import json
from itemadapter import ItemAdapter



class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open('items.json', 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item

class CsvWriterPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        print("CsvWriterPipeline spider has been open")
        self.file = open('output.csv', 'a+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        print("CsvWriterPipeline spider has been close")
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        #print(item)
        self.exporter.export_item(item)
        return item

from myProject.database import Items, create_items_table, db_connect
from sqlalchemy.orm import sessionmaker
class PostgresSQLStorePipeline(object):


    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates items table.
        """
        engine = db_connect()
        create_items_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Process the item and store to database.
        """
        session = self.Session()
        instance = session.query(Items).filter_by(**item).one_or_none()
        if instance:
            return instance
        zelda_item = Items(**item)

        try:
            session.add(zelda_item)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

