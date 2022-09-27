import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
import json
import base64

class CartierSpider(scrapy.Spider):
    name = 'adds'
    

    def start_requests(self):
        url = 'https://www.whatmobile.com.pk/'
        splash_args = {
        'html': 1,
        'png': 1,
        'width': 1080,
        'wait':20,
        'render_all':1
    }
        yield SplashRequest(url=url, callback=self.parse,
                        endpoint="render.json",
                        args=splash_args)
    def parse(self, response):
        imgdata = base64.b64decode(response.data['png'])
        filename = 'image.png'
        with open(filename, 'wb') as f:
            f.write(imgdata)


    