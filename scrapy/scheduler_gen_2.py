from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
# https://stackoverflow.com/questions/44228851/scrapy-on-a-schedule
from configparser import ConfigParser
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from myProject import trim_data_gen_2 as dataCrawler


symbols = [
    'TWB',
    'VM',
    'WCIMQ',
]

from apscheduler.schedulers.twisted import TwistedScheduler
scheduler = TwistedScheduler()



def run_crawl():
    """
    Run a spider within Twisted. Once it completes,
    wait ? seconds and run another spider.
    """
    s = get_project_settings()
    s.update({
      "LOG_ENABLED": "True",
      'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
      "SPIDER_MODULES" :['myProject'],
      "FEED_EXPORTERS" :{
          'csv': 'myProject.exporters.CsvItemExporter',
      } ,
      'scrapy.extensions.telnet.TelnetConsole': None,
      "ITEM_PIPELINES" :{
          'myProject.pipeline.PostgresSQLStorePipeline': 300,
          'myProject.pipeline.JsonWriterPipeline': 800,
      }
    })
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    print("Getting information from config.ini")
    #Read config.ini file
    config_object = ConfigParser()
    config_object.read("config.ini")
    #Get the password
    cfg = config_object["CFG"]
    print("apikey is {}".format(cfg["apikey"]))
    # convert the counter to int
    apikey=cfg["apikey"]
    symbolCounter=int(cfg["stocksymbollistcounter"])

    if symbolCounter > 2:
        print("No more symbols to process.")
        scheduler.remove_job('my_job_id')
        scheduler.shutdown()
        
    else:
        print("Now Dealing with the Stock",symbols[symbolCounter], ".")
        start_urls = ['https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED'
                        '&symbol='+symbols[symbolCounter]+
                        '&apikey='+apikey+
                        '&datatype=json']
        runner = CrawlerRunner(s)
        deferred = runner.crawl(dataCrawler.MonsterSpiderSpider,start_url= start_urls[0], output="target-stocks.csv")
        # Update the counter
        symbolCounter=symbolCounter+1
        cfg["stocksymbollistcounter"] = str(symbolCounter)
        # Write changes back to file
        with open('config.ini', 'w') as conf:
            config_object.write(conf)
        print(deferred)
        return deferred
        
scheduler.add_job(run_crawl, 'interval',  seconds=20,id='my_job_id')
scheduler.start()
reactor.run()
