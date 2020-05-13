import scrapy
from scrapy.crawler import CrawlerProcess
import re
from datetime import date
import Scraping.items
from lmn.models import Show, Venue, Artist

"""  This is the file for the show spider. A spider is a program that crawls a webpage and scrapes information from it.  """

def add_months(num_of_months):
    """ A helper method to find what month and year it is after adding or subtracting a given number or months from the day's date. This is used by the ShowSpider class to generate the starting URLs, which in first ave's website are based on the month and year. """
    today = date.today()
    month = today.month + num_of_months
    year = today.year

    if month < 1 or month > 12: 
        # the num_months / abs(num_months) is to get the sign (+/-) of the number of months and add / subtract accordingly.
        month += 12 * -(num_of_months / abs(num_of_months))
        year += 1 * (num_of_months / abs(num_of_months))

    return [int(year), int(month)]

class ShowSpider(scrapy.Spider):
    """ This spider is figures out a list of starting URLs using the add_months method, and uses them to get the name, venue, time, ages, date and URL of all shows listed on that page. """
    name = 'show'
    today = date.today()
    custom_settings = {
        'ITEM_PIPELINES' : {
            'Scraping.pipelines.ShowPipeline': 300
        } 
    }

    start_urls = []

    for x in range(-3, 6): # This range determines how many months into the past and future you are going to scrape.
        year_month = add_months(x)
        start_urls.append('https://first-avenue.com/calendar/all/{year}-{month}'.format(year = year_month[0], month = year_month[1]))

    def parse(self, response):
        """ The parse method takes the response from the spider, being the pages whole HTML, and reads through it looking for the show's information, which it saves into an event item which it checks to see if the venue is already in the database. If the venue doesn't exist, it sends the event's url request to venue_parser_1. If it does, the event url request as well as the event itsef is sent to parse_artist to get the show artist and date. """
        # Gets the page's body and saves it as a string.
        page = response.css('body').get()
        
        # Get's the url, name, venue name, show time, and age catagory from the page.
        matches = re.findall("\"field-item even\"><a href=\"(/event[^\"]+)\">([^<]+)[\s\S]+?a href=\"/venue[^\"]+[^>]+>([^<]+)[\s\S]+?\"date-display-single[^>]+>([^<]+)[\s\S]+?even\">([^<]+)", page)
        print('TEST')
        for match in matches:
            event = Scraping.items.Event(url = 'https://first-avenue.com' + match[0], name = match[1], venue = match[2], time = match[3], ages = match[4])

            # First Avenue is sometimes called something else on the show page. Because 7th street entry and mainroom do not have their own venue pages, they can never be added to the database and anything with them listed will not be added to the database as a result unless we fix their names.
            if event['venue'] == '7th St Entry' or event['venue'] == 'Mainroom':
                event['venue'] = 'First Avenue'
            if not Venue.objects.filter(name = event['venue']).exists():
                yield scrapy.Request(url=event['url'], callback=self.parse_venue_1, method="GET", priority=1)

            request = scrapy.Request(url=event['url'], callback=self.parse_artist, method="GET", priority=1, cb_kwargs=dict(main_url=response.url))
            request.cb_kwargs['event'] = event
            yield request


    def parse_venue_1(self, response):
        """ The parse_venue_1 method reads through the event's page to find the url for the venue which it sends a request of to the parse_venue_2 method. """
        # Gets the page's body and saves it as a string.
        page = response.css('body').get()

        # Gets the venue's URL.
        match = re.search("Venue:[\s\S]+?a href=\"([^\"]+)", page)
        venue_url = match[1]

        yield scrapy.Request(url='https://first-avenue.com' + venue_url, callback=self.parse_venue_2, method="GET", priority=1)

    def parse_venue_2(self, response):
        """ The parse_venue_2 method reads through the venue's page to find the city and statee for the venue which it saves into a venue item and sends to the pipeline for processing. """
        # Gets the page's body and saves it as a string.
        venue_page = response.css('body').get()

        # Gets the name, city, and state of the venue.
        match = re.search("id=\"page-title\">([^<]+)[\s\S]+?\"locality\">([^<]+)[^>]+>[^>]+>([^<]+)", venue_page)
        venue_name = match[1].strip()
        venue_city = match[2].strip()
        venue_state = match[3].strip()

        venue = Scraping.items.Venue(name=venue_name, city=venue_city, state=venue_state)
        yield(venue)

    def parse_artist(self, response, main_url, event):
        """ The parse_artist method reads through the event's page to find the artist and date of the event, which it saves into the event object it was given from the origional parse method and sends to the pipeline for processing. """
        # Gets the page's body and saves it as a string.
        page = response.css('body').get()

        # Attempts to get the artist and date of show.
        match = re.search("\"performers\">([^<]+)[\s\S]+?datepart\">([^<]+)", page)
        if match:
            name = match[1].strip()
            date = match[2].strip()
        else:
            # Gets the artist and date of event if it's formatted the other way.
            match = re.search("datepart\">([^<]+)[\s\S]+?Presented by:[\d\D]+?>([^<]+)", page)
            name = match[2].strip()
            date = match[1].strip()
        event['artist'] = name
        event['date']   = date
        yield event
