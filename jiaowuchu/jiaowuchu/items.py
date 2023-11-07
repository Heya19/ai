# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JiaowuchuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    section = scrapy.Field()

    post_time = scrapy.Field()
    brief = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    attachment = scrapy.Field()



