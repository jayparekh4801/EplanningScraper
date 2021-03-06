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
        next_page = response.xpath('//ul[@class = "pagination"]/li[@class = "active"]/following-sibling::li[1]/a/@href').get()
        next_page = response.urljoin(next_page)
        table = response.xpath('//table')
        rows = table.xpath('.//tr')

        for ind, row in enumerate(rows) :
            if(ind == 0) :
                continue
                
            application_url = row.xpath('./td[1]/a/@href').get()
            application_url = response.urljoin(application_url)
            yield scrapy.Request(url=application_url, callback=self.parse_agent)
            # for scraping table
            # yield {
            #     "link" : row.xpath('./td[1]/a/@href').get(),
            #     "app_status" : row.xpath('./td[2]/text()').get(),
            #     "due_date" : row.xpath('./td[3]/text()').get(),
            #     "date" : row.xpath('./td[4]/text()').get(),
            #     "decidsion_code" : row.xpath('./td[5]/text()').get(),
            #     "received_date" : row.xpath('./td[6]/text()').get(),
            #     "app_name" : row.xpath('./td[7]/text()').get(),
            #     "dev_add" : row.xpath('./td[8]/text()').getall(),
            #     "dev_desc" : row.xpath('./td[9]/text()').get(),
            #     "lo_auth_name" : row.xpath('./td[10]/text()').get()
            # }
        # print(next_page)
        # both works
        yield scrapy.Request(next_page, callback = self.parse_pages)
        # yield response.follow(url=next_page, callback=self.parse_pages)
    
    def parse_agent(self, response) :
        agent = response.xpath('//input[@title = "Show Agents Popup"]/@style').get()
        if(agent == "display: inline;  visibility: visible;") :
            name = response.xpath('//tr[./th/text() = "Name :"]/td/text()').get()
            address = response.xpath('//tr[./th/text() = "Address :"]/following-sibling::tr/td//text()').getall()[0:3]
            phone = response.xpath('//tr[./th/text() = "Phone :"]/td/text()').get()
            fax = response.xpath('//tr[./th/text() = "Fax :"]/td/text()').get()
            email = response.xpath('//tr[./th/text() = "e-mail :"]/td//text()').get()
            yield {
                "name" : name,
                "address" : address,
                "phone" : phone,
                "fax" : fax,
                "email" : email
            }
            pass
        # //div[@id = "DivAgents"]/table//tr[./th/text() = "Address :"]/following-sibling::tr[1]
        else : 
            self.logger.info("button not present -----------------")