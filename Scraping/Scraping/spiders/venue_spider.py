import scrapy
from scrapy.crawler import CrawlerProcess
import re
from ..items import Venue

class VenueSpider(scrapy.Spider):
    name = 'venue'
    today = date.today()
    allowed_domains = 'https://first-avenue.com/'
    custom_settings = {
        'ITEM_PIPELINES' : {
            'Scraping.pipelines.VenuePipeline': 300
        } 
    }

    def __init__(self, url, *args, **kwargs):
        self.start_urls = [url]
        self.logger.info(self.start_urls)
        super(VenueSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # Get the page and saves it as a string.
        page = response.css('body').get()

        match = re.find("Venue:[\s\S]+?a href=\"([^\"]+)\">([^<]+)", page)
        venue_url = match[0]
        venue_name = match[1]

        venue_response = scrapy.Request(url = venue_url)
        venue_page = venue_response.css('body').get()

        match = re.find("\"locality\">([^<]+)[^>]+>[^>]+>([^<]+)", venue_page)
        venue_city = match[0]
        venue_state = match[1]

        venue = Venue(name=venue_name, city=venue_city, state=venue_state)
        yield venue