import scrapy

class CrawlingSpider(scrapy.Spider):
    name = 'mycrawler'
    start_urls = ['https://nhadat24h.net/nha-dat-ban']
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,dont_filter=False)

    def parse(self,response):
        for items in response.css("div.dv-item"):
            yield {
                'title': response.css('div.pn1 a::attr(title)').get(),
                #'time' : response.css('p.time::text').get(), #with respect to current time of browsed => Fix later
                #'price': response.css('label.a-txt-cl1::text').get(),
                #'area' :response.css('label.a-txt-cl2::text').get(),
                #'neighborhood': response.css('label.rvVitri ::text').get(),
                #'description' : response.css('label.lb-des ::text').get()
            }
        next_page = response.css('div.dv-pt-item  a::attr(href)').getall()[1]
        if next_page is not None:
            yield response.follow(next_page,callback = self.parse)