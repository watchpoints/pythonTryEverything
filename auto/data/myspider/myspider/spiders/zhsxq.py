import scrapy


class ZhsxqSpider(scrapy.Spider):
    """
        知识星球
    """
    name = "zhsxq"
    allowed_domains = ["wx.zsxq.com"]
    start_urls = ["https://wx.zsxq.com/group/88885284844882"]
     
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'playwright': True,
                'playwright_include_page': True,
            })

    def parse(self, response):
            # iterate over the product elements
            for product in response.css(".post"):
                # scrape product data
                url = product.css("a").attrib["href"]
                image = product.css(".card-img-top").attrib["src"]
                name = product.css("h4 a::text").get()
                price = product.css("h5::text").get()
    
                # add the data to the list of scraped items
                yield {
                    "url": url,
                    "image": image,
                    "name": name,
                    "price": price
                }

