# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from ...lmn.models import Show, Venue, Artist
from Scraping.Scraping.spiders.venue_spider import VenueSpider
from scrapy.crawler import CrawlerProcess

class VenuePipeline(object):
    def process_item(self, item, spider):
        Venue(name=item['name'], city=item['city'], state=item['state'])
        Venue.save

class ShowPipeline(object):
    def process_item(self, item, spider):
        # checks if new artist exists, makes them if they don't 
        if not Artist.objects.filter(name = item['artist']).exists():
            new_artist = Artist(name = item['artist'])
            new_artist.save()
        
        if not Venue.objects.filter(name = item['venue']):
            process = CrawlerProcess()
            process.crawl(VenueSpider, url = item['url'])
            process.start()
        # check if Venue exists, make one if not
            # go to URL and find venue information.

        Show(artist = item['artist'], venue = item['venue'], name = item['name'], url = item['url'], time = item['time'], ages = item['ages'], show_date = item['show_date'])
        Show.save()
        return item
