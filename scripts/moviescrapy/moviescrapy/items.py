# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    name = scrapy.Field()
    avg_movie_score = scrapy.Field()
    number_of_movie_reviews = scrapy.Field()

class ReviewItem(scrapy.Item):
    movie = scrapy.Field()
    user = scrapy.Field()
    score = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()
    scrape_date = scrapy.Field()
    url = scrapy.Field()

