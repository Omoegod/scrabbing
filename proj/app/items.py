# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class Repositories(scrapy.Item):
    rep_name = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    stars = scrapy.Field()
    forks = scrapy.Field()
    watching = scrapy.Field()
    commits = scrapy.Field()
    info_commit = scrapy.Field()
    releases = scrapy.Field()
    info_releases = scrapy.Field()