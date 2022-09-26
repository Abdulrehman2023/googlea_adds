import scrapy
import time 
class TestSpider(scrapy.Spider):
    name = "test"


    

    def start_requests(self):
        start_urls = [
        "https://www.giveme5.co/",
    ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            print("-----------------Request Send------------------------")
            time.sleep(20)
            
            
            


    def parse(self, response):
        print("-----------------Crawlled------------------------")
        
        filename = response.url.split("/")[-1] + 'file.html'
        with open(filename, 'wb') as f:
            f.write(response.body)


