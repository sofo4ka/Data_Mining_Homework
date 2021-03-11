# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GbParseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GbAutoYoulaItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    photos = scrapy.Field()
    characteristics = scrapy.Field()
    descriptions = scrapy.Field()
    author = scrapy.Field()


class InstagramTagItem(scrapy.Item):
    url = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    allow_following = scrapy.Field()
    is_following = scrapy.Field()
    is_top_media_only = scrapy.Field()
    profile_pic_url = scrapy.Field()
    edge_hashtag_to_top_posts = scrapy.Field()

# class HhparseItem(scrapy.Item):
#     _id = scrapy.Field()
#     vacancy_title = scrapy.Field()
#     salary = scrapy.Field()
#     description = scrapy.Field()
#     key_skills = scrapy.Field()
#     author = scrapy.Field()
#     author_info = scrapy.Field()
