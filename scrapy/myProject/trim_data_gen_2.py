import scrapy
import json

class Stock_Object(scrapy.Item):
    Date = scrapy.Field()
    Symbol = scrapy.Field()
    Monthly_Adjusted_Value = scrapy.Field()
    Open = scrapy.Field()
    High = scrapy.Field()
    Low = scrapy.Field()
    Volume = scrapy.Field()
    Dividend_Amount = scrapy.Field()


class MonsterSpiderSpider(scrapy.Spider):
    name = 'project'
    allowed_domains = ['alphavantage.co']

    results = []
    
    def __init__(self, *args, **kwargs): 
        super(MonsterSpiderSpider, self).__init__(*args, **kwargs) 
        # overwrite the start url
        self.start_urls = [kwargs.get('start_url')] 
        
    def parse(self, response):
        print("running")
        try:
            results = json.loads(response.body)
            print(results)
            stock_symbol = results['Meta Data']['2. Symbol']
            final_csv_output= []
            for result in results["Monthly Adjusted Time Series"]:
                detail = Stock_Object()
                detail["Date"] = result
                detail["Symbol"] = stock_symbol
                detail["Monthly_Adjusted_Value"] = results['Monthly Adjusted Time Series'][result]["5. adjusted close"]
                detail["Open"] = results['Monthly Adjusted Time Series'][result]["1. open"]
                detail["High"] = results['Monthly Adjusted Time Series'][result]["2. high"]
                detail["Low"] = results['Monthly Adjusted Time Series'][result]["3. low"]
                detail["Volume"] = results['Monthly Adjusted Time Series'][result]["6. volume"]
                detail["Dividend_Amount"] = results['Monthly Adjusted Time Series'][result]["7. dividend amount"]
                yield detail
                #final_csv_output.append(detail)
            # Use yield instead of return
            # yield will pass into Pipeline
            
            return final_csv_output
        except ValueError:
          print("Oops!  That was no valid number.  Try again...")
            

