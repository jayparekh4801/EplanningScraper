import scrapy
from selenium import webdriver


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
        data = {
        }
        pass