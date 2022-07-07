# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class Repositories(scrapy.Item):
    rep_url = scrapy.Field()
    username = scrapy.Field()
    rep_name = scrapy.Field()
    description = scrapy.Field()
    stars = scrapy.Field()
    forks = scrapy.Field()
    watching = scrapy.Field()
    url = scrapy.Field()
    commits = scrapy.Field()
    author_commit = scrapy.Field()
    name_commit = scrapy.Field()
    datetime_commit = scrapy.Field()
    releases = scrapy.Field()
    version_releases = scrapy.Field()
    datetime_releases = scrapy.Field()
    changelog_releases  = scrapy.Field()