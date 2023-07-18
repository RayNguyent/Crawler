import scrapy

class CrawlingSpider(scrapy.Spider):
    name = 'mycrawler'
    start_urls = ['https://nhadat24h.net/nha-dat-ban',
                'https://nhadat24h.net/nha-dat-cho-thue']
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,dont_filter=False)

    def parse(self,response):
        for link in response.css("div.dv-item a.a-title::attr(href)"):
            yield response.follow(link.get(), callback = self.parse_items)
            
            
        next_page = response.css('div.dv-pt-item  a::attr(href)').getall()[-1]
        if next_page is not None:
            yield response.follow(next_page,callback = self.parse)


    def parse_items(self,response):   
        raw_images_urls = response.css('li a.swipebox::attr(href)').getall()
        clean_img_urls = []
        for img_url in raw_images_urls:
            clean_img_urls.append(response.urljoin(img_url))
        yield {
            'title': response.css('#txtcontenttieudetin::text').get(),
            'type': response.css('#ContentPlaceHolder1_ctl00_lbLoaiBDS::text').get(),
            'time' : response.css('p.time::text').get(), 
            'price': ' '.join([response.css('.strong1::text').get(),response.css("label.lb-pri-dt").get().split('</label')[1].split('>')[1].split(' ')[0]]),
            'area' : ' '.join([response.css('.strong2::text').get(),response.css("label.lb-pri-dt").get().split('</label')[2].split('>')[1]]),
            'land_title_certificate': response.css(".dv-time-dt strong::text").get(),
            'location': response.css("#ContentPlaceHolder1_ctl00_lbTinhThanh::text").get(),
            'description' : '  '.join(response.css(".dv-txt-mt ::text").getall()),
            'beds': response.css('.dv-time-dt+ .dv-tsbds tr:nth-child(1) .col1+ td').get().split('<td>')[1].split('</td>')[0],
            'floors': response.css('.dv-tsbds:nth-child(5) tr:nth-child(1) .col1+ td').get().split('<td>')[1].split('</td>')[0],
            'road_width': response.css('.dv-tsbds:nth-child(6) tr:nth-child(1) .col1+ td').get().split('<td>')[1].split('</td>')[0],
            'parking_slots': response.css('.dv-tsbds:nth-child(7) tr:nth-child(1) .col1+ td').get().split('<td>')[1].split('</td>')[0],
            'washrooms': response.css('.dv-time-dt+ .dv-tsbds tr+ tr .col1+ td').get().split('<td>')[1].split('</td>')[0],
            'direction': response.css('#ContentPlaceHolder1_ctl00_lbHuong::text').get(),
            'land_width': response.css('.dv-tsbds:nth-child(6) tr+ tr .col1+ td').get().split('<td>')[1].split('</td>')[0],
            'id': response.css('.dv-tsbds:nth-child(7) tr+ tr .col1+ td').get().split('<td>')[1].split('</td>')[0],
            'seller': response.css('.fullname a::text').get(),
            'company': response.css('.fullname+ label::text').get(),
            'contact':response.css('#viewmobinumber::text').get(),
            'image_urls': clean_img_urls,
        }