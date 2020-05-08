import scrapy
from scrapy.crawler import CrawlerProcess
import re
from datetime import date
from ..items import Event
all_events = []

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

    for x in range(-3, 4): # This range determines how many months into the past and future you are going to scrape.
        year_month = add_months(x)
        start_urls.append('https://first-avenue.com/calendar/all/{year}-{month}'.format(year = year_month[0], month = year_month[1]))

    def parse(self, response):
        """ The parse method takes the response from the spider, being the pages whole HTML, and reads through it looking for the show's information, which it saves into an event item to send to the ShowPipeline for processing. """
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
                yield(event)

# all of this is for testing purposes. To be deleted in final code.
"""print(all_events)

process = CrawlerProcess()
process.crawl(ShowSpider)
process.start()

print()
print(all_events[1])
"""
