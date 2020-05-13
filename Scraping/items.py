""" Items are objects for spiders to save data into. """

import scrapy

class Event(scrapy.Item):
    """ The event item stores show information from the show spider """
    name   = scrapy.Field()
    artist = scrapy.Field()
    venue  = scrapy.Field()
    url    = scrapy.Field()
    time   = scrapy.Field()
    ages   = scrapy.Field()
    date   = scrapy.Field()

class Venue(scrapy.Item):
    """ The venue item stores venue information from the show spider's parse venue methods """
    name   = scrapy.Field()
    city   = scrapy.Field()
    state  = scrapy.Field()

class Artist(scrapy.Item):
    """ The artiest item stores artist information from the show spider's parse artist method """
    name   = scrapy.Field()