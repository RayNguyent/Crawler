import scrapy

class CrawlingSpider(scrapy.Spider):
    name = 'mycrawler'
    start_urls = ['https://nhadat24h.net/nha-dat-cho-thue']
    
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
            'Data source': 'https://nhadat24h.net/nha-dat-cho-thue',
            'Agent': 'Hoang Nguyen',
            'Category': 'rent',
            'ID': response.css('.dv-tsbds:nth-child(7) tr+ tr .col1+ td').get().split('<td>')[1].split('</td>')[0],
            'Title': response.css('#txtcontenttieudetin::text').get(),
            'Post link': response.request.url,
            'Price': ' '.join([response.css('.strong1::text').get(),response.css("label.lb-pri-dt").get().split('</label')[1].split('>')[1].split(' ')[0]]),
            'Area' : ' '.join([response.css('.strong2::text').get(),response.css("label.lb-pri-dt").get().split('</label')[2].split('>')[1]]),
            'Location': response.css("#ContentPlaceHolder1_ctl00_lbTinhThanh::text").get(),
            'Estate type': response.css('#ContentPlaceHolder1_ctl00_lbLoaiBDS::text').get(),
            'Direction': response.css('#ContentPlaceHolder1_ctl00_lbHuong::text').get(),
            'Rooms': '',
            'Bedrooms': response.css('.dv-time-dt+ .dv-tsbds tr:nth-child(1) .col1+ td').get().split('<td>')[1].split('</td>')[0],
            'Kitchen': '',
            'Living room': '',
            'Bathrooms': response.css('.dv-time-dt+ .dv-tsbds tr+ tr .col1+ td').get().split('<td>')[1].split('</td>')[0],
            'Front_width': response.css('.dv-tsbds:nth-child(6) tr+ tr .col1+ td').get().split('<td>')[1].split('</td>')[0],
            'Floor': response.css('.dv-tsbds:nth-child(5) tr:nth-child(1) .col1+ td').get().split('<td>')[1].split('</td>')[0],
            'Parking Slot': response.css('.dv-tsbds:nth-child(7) tr:nth-child(1) .col1+ td').get().split('<td>')[1].split('</td>')[0],
            'Description' : '  '.join(response.css(".dv-txt-mt ::text").getall()),
            'Seller name': response.css('.fullname a::text').get(),
            'Seller type': response.css('.fullname+ label::text').get(),
            'Phone':response.css('#viewmobinumber::text').get(),
            'image_urls': clean_img_urls,
            'Email': '',
            'Road width': response.css('.dv-tsbds:nth-child(6) tr:nth-child(1) .col1+ td').get().split('<td>')[1].split('</td>')[0],
            'Sizes': '',
        }