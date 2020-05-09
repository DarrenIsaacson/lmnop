import scrapy
from scrapy.crawler import CrawlerProcess
import re
from ..items import Venue
from datetime import date
""" This is the file for the venue spider. A spider is a program that crawls a webpage and scrapes information from it. """

class VenueSpider(scrapy.Spider):
    """ This spider is given the URL of a show, and uses it to get the name and URL of the show's venue. It then goes to the venue's URL and get's the venue's location. """
    name = 'venue'
    today = date.today()
    #allowed_domains = 'https://first-avenue.com/'
    custom_settings = {
        'ITEM_PIPELINES' : {
            'Scraping.pipelines.VenuePipeline': 200
        } 
    }

    def __init__(self, url, *args, **kwargs):
        self.start_urls = [url]
        self.logger.info(self.start_urls)
        super(VenueSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        """ The parse method takes the response from the spider, being the pages whole HTML, and reads through it looking for the venue's name and URL. From that URL it gets a new response which it looks through for the city and state of the venue which it saves into a venue item to send to the ShowPipeline for processing. """
        page = response.css('body').get()

        match = re.search("Venue:[\s\S]+?a href=\"([^\"]+)", page)
        venue_url = match[1]

        print('TEST:' + venue_url)
        yield scrapy.Request('https://first-avenue.com' + venue_url, callback=self.parse_venue_page, method="GET")

    def parse_venue_page(self, response):
        venue_page = response.css('body').get()

        print('TEST!!!')

        match = re.search("id=\"page-title\">([^<]+)[\s\S]+?\"locality\">([^<]+)[^>]+>[^>]+>([^<]+)", venue_page)
        venue_name = match[1]
        venue_city = match[2]
        venue_state = match[3]

        venue = Venue(name=venue_name, city=venue_city, state=venue_state)
        yield(venue)