from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = 'mycrawler'
    allow_domains = ['.com.vn']
    start_urls = ['https://batdongsan24h.com.vn']

    rules = (
        Rule(LinkExtractor(allow='bat-dong-san-ban-tai-viet-nam-s32113')),
        Rule(LinkExtractor(allow='bat-dong-san-cho-thue-tai-viet-nam-s34397')),

    )
