import scrapy
from selenium import webdriver
from scrapy.http import FormRequest

class EplannigSpider(scrapy.Spider):
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    def parse(self, response):
        urls = response.xpath('//a[@target = "_blank"]/@href').getall()

        for url in urls :
            yield response.follow(url = url, callback = self.parse_url)
    
    def parse_url(self, response) :
        url = response.xpath('//span[contains(@class, "glyphicon glyphicon-inbox btn-lg")]/following-sibling::a/@href').get()
        yield response.follow(url = url, callback = self.parse_form)

    def parse_form(self, response) :
        yield FormRequest.from_response(response=response, 
                                  formdata= {
                                      'RdoTimeLimit' : '42'
                                  },
                                  dont_filter = True,
                                  formxpath='(//form)[2]',
                                  callback = self.parse_pages)
        
    
    def parse_pages(self, response) :
        pass