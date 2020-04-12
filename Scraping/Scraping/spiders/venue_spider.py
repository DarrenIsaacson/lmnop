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

    first_concert_month = today.month - 6
    first_concert_year = today.year
    if first_concert_month < 1:
        first_concert_month += 12
        first_concert_year -= 1

    start_urls = []

    for x in range(-3, 4):
        year_month = add_months(x)
        start_urls.append('https://first-avenue.com/calendar/all/{year}-{month}'.format(year = year_month[0], month = year_month[1]))

    def parse(self, response):
        page = response.css('body').get()

        dates = re.findall("<h3><div class=\"date-repeat-instance\"><span class=\"date-display-single\">([^<]+)([\s\S]+?)</article><!-- /.node -->", page)
        for date in dates:
            matches = re.findall("\"field-item even\"><a href=\"(/event[^\"]+)\">([^<]+)[\s\S]+?a href=\"/venue[^\"]+\">([^<]+)[\s\S]+?\"date-display-single\">([^<]+)[\s\S]+?even\">([^<]+)", date[1])
        
            for match in matches:
                event = Event(url = 'https://first-avenue.com' + match[0], name = match[1], venue = match[2], time = match[3], ages = match[4], date = date[0])
                all_events.append(event)

        """next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)"""


print(all_events)

process = CrawlerProcess()
process.crawl(VenueSpider)
process.start()

print()
print(all_events[1])