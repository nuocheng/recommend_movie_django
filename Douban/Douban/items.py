# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    typeid=scrapy.Field()
    typename=scrapy.Field()
    rate=scrapy.Field()
    title=scrapy.Field()
    url=scrapy.Field()
    cover=scrapy.Field()
    movieid=scrapy.Field()
    is_new=scrapy.Field()

class MovieItem(scrapy.Item):
    movieid=scrapy.Field()
    movieicon=scrapy.Field()
    moviename=scrapy.Field()
    movieauteur=scrapy.Field()
    movieauteur_url=scrapy.Field()
    moviemake=scrapy.Field()
    moviemake_url=scrapy.Field()
    movieactor=scrapy.Field()
    movieactor_url=scrapy.Field()
    movietype=scrapy.Field()
    moviecountry=scrapy.Field()
    movielanguage=scrapy.Field()
    movieon=scrapy.Field()
    moviedesc=scrapy.Field()
    url=scrapy.Field()

class actorItem(scrapy.Item):
    name = scrapy.Field()
    icon=scrapy.Field()
    gender = scrapy.Field()
    birth_date = scrapy.Field()
    birth_where = scrapy.Field()
    profession = scrapy.Field()
    imdb = scrapy.Field()
    url=scrapy.Field()

class auteurItem(scrapy.Item):
    name=scrapy.Field()
    icon=scrapy.Field()
    gender=scrapy.Field()
    birth_date=scrapy.Field()
    birth_where=scrapy.Field()
    profession=scrapy.Field()
    imdb=scrapy.Field()
    url=scrapy.Field()

class make_moiveItem(scrapy.Item):
    name = scrapy.Field()
    icon = scrapy.Field()
    gender = scrapy.Field()
    birth_date = scrapy.Field()
    birth_where = scrapy.Field()
    profession = scrapy.Field()
    imdb = scrapy.Field()
    url = scrapy.Field()

class movie_auteur(scrapy.Item):
    movieid=scrapy.Field()
    auteurid=scrapy.Field()

class movie_actor(scrapy.Item):
    movieid=scrapy.Field()
    actorid=scrapy.Field()
