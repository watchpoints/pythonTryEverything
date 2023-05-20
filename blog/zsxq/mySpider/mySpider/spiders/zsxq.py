import scrapy


class ZsxqSpider(scrapy.Spider):
    name = "zsxq"
    allowed_domains = ["zsxq.com"]
    start_urls = ["http://zsxq.com/"]

    def parse(self, response):
        pass
