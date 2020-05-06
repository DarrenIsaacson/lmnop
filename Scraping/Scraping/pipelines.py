# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from ...lmn.models import Show, Venue, Artist
from Scraping.Scraping.spiders.venue_spider import VenueSpider
from scrapy.crawler import CrawlerProcess

class VenuePipeline(object):
    # takes the information gathered by the venue spider and makes a venue from it.
    def process_item(self, item, spider):
        Venue(name=item['name'], city=item['city'], state=item['state'])
        Venue.save
        return item

class ShowPipeline(object):
    def process_item(self, item, spider):
        # checks if artist exists, makes them if they don't. 
        if not Artist.objects.filter(name = item['artist']).exists():
            new_artist = Artist(name = item['artist'])
            new_artist.save()
        
        # checks if venue exists, if not runs the venue spider to get the name, city, and state of the venue.
        if not Venue.objects.filter(name = item['venue']).exists():
            process = CrawlerProcess()
            process.crawl(VenueSpider, url = item['url'])
            process.start()

        Show(artist = item['artist'], venue = item['venue'], name = item['name'], url = item['url'], time = item['time'], ages = item['ages'], show_date = item['show_date'])
        Show.save()
        return item
