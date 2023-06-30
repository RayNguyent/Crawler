import scrapy

class CrawlingSpider(scrapy.Spider):
    name = 'mycrawler'
    start_urls = ['https://nhadat24h.net/nha-dat-ban',
                'https://nhadat24h.net/nha-dat-cho-thue']
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,dont_filter=False)

    def parse(self,response):
        for items in response.css("div.dv-item"):
            raw_images_urls = items.css('img.imageThumb1::attr(data-src)').getall()
            clean_img_urls = []
            for img_url in raw_images_urls:
                clean_img_urls.append(response.urljoin(img_url))
            yield {
                'title': items.css('div.pn1 a span::text').get(),
                'time' : items.css('p.time::text').get(), #with respect to current time of browsed => Fix later
                'price': items.css('label.a-txt-cl1::text').get(),
                'area' : items.css('label.a-txt-cl2::text').get(),
                'locationfet': items.css('label.rvVitri ::text').get(),
                'description' : items.css('label.lb-des ::text').get(),
                'seller': items.css('div.fullname::text').get(),
                'image_urls': clean_img_urls,
            }
        next_page = response.css('div.dv-pt-item  a::attr(href)').getall()[-1]
        if next_page is not None:
            yield response.follow(next_page,callback = self.parse)