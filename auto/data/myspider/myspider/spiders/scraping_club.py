import scrapy


class ScrapingClubSpider(scrapy.Spider):
    name = "scraping_club"
    allowed_domains = ["scrapingclub.com"]
    start_urls = ["https://scrapingclub.com/exercise/list_infinite_scroll/"]
    
    def start_requests(self):
            url = "https://scrapingclub.com/exercise/list_infinite_scroll/"
            yield scrapy.Request(url, meta={"playwright": True})

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
