import scrapy
from scrapy.crawler import CrawlerProcess
import re
from datetime import date
#from ..items import Event
all_events = []

def add_months(num_of_months):
    today = date.today()
    month = today.month + num_of_months
    year = today.year

    if month < 1 or month > 12: 
        # the num_months / abs(num_months) is to get the sign (+/-) of the number of months and add / subtract accordingly.
        month += 12 * -(num_of_months / abs(num_of_months))
        year += 1 * (num_of_months / abs(num_of_months))

    return [int(year), int(month)]

class Event(scrapy.Item):
    # this will be in items.py in final, but for testing purposes I was having trouble importing it so I just pasted it here.
    name = scrapy.Field()
    artist = scrapy.Field()
    venue = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    ages = scrapy.Field()
    date = scrapy.Field()

class VenueSpider(scrapy.Spider):
    name = 'venues'
    today = date.today()

    start_urls = []

    for x in range(-3, 4): # This range determines how many months into the past and future you are going to scrape.
        year_month = add_months(x)
        start_urls.append('https://first-avenue.com/calendar/all/{year}-{month}'.format(year = year_month[0], month = year_month[1]))

    def parse(self, response):
        # Get the page and saves it as a string.
        page = response.css('body').get()

        # Uses a regex statement to get all the dates
        dates = re.findall("<h3><div class=\"date-repeat-instance\"><span class=\"date-display-single\">([^<]+)([\s\S]+?)</article><!-- /.node -->", page)
        for date in dates:
            # Uses a regex statement to get all the shows on each date.
            matches = re.findall("\"field-item even\"><a href=\"(/event[^\"]+)\">([^<]+)[\s\S]+?a href=\"/venue[^\"]+\">([^<]+)[\s\S]+?\"date-display-single\">([^<]+)[\s\S]+?even\">([^<]+)", date[1])
        
            # Saves the show data into all_events
            for match in matches:
                event = Event(url = 'https://first-avenue.com' + match[0], name = match[1], venue = match[2], time = match[3], ages = match[4], date = date[0])
                all_events.append(event)

#all of this is for testing purposes. To be deleted in final code.
print(all_events)

process = CrawlerProcess()
process.crawl(VenueSpider)
process.start()

print()
print(all_events[1])