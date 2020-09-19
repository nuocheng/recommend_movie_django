# -*- coding: utf-8 -*-
import scrapy
import json
import time
import re
import random
from ..items import  DoubanItem,MovieItem,actorItem,auteurItem,make_moiveItem,movie_auteur,movie_actor
from urllib.parse import urlencode

"""
https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0
https://movie.douban.com/j/search_subjects?type=movie&tab=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0

"""
class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/j/search_tags?type=movie&tag=%E6%9C%80%E6%96%B0&source=index']

    def parse(self, response):
        jsons_data=json.loads(response.text)['tags']
        print(jsons_data)
        print(len(jsons_data))
        for tag in jsons_data:
            data={
                "type":"movie",
                "tag":tag,
                "page_limit":50,
                "page_start":0
            }
            url="https://movie.douban.com/j/search_subjects?"+urlencode(data)
            # print(url)
            time.sleep(round(random.uniform(0, 1), 2))
            yield scrapy.Request(url,callback=self.parse_detail,meta={"item":tag})

    #电影连接信息
    def parse_detail(self,response):
        tag=response.meta['item']
        json_data=json.loads(response.text)['subjects']
        for info in json_data:
            item=DoubanItem()
            item['typename']=tag
            item['rate']=info['rate']
            item['title']=info['title']
            item['url']=info['url']
            item['cover']=info['cover']
            item['movieid']=info['id']
            item['is_new']=info['is_new']
            time.sleep(round(random.uniform(0,1),2))
            yield scrapy.Request(item['url'],callback=self.parse_movie,meta={"item":item})
    #电影详细信息
    def parse_movie(self,response):
        #电影部分信息
        # a = lambda x, y: {"name": x, "url": "https://movie.douban.com" + y}
        item=response.meta['item']
        movie = MovieItem()
        movie['movieid'] = item["movieid"]
        movie['movieicon'] = item['cover']
        movie['moviename'] = item['title']
        movie['url']=item['url']
        movie['movieid']=item['movieid']
        
        print({
            "movieid":movie['movieid'],
            "moviename":movie['moviename'],
            "url":movie['url'],
            "icon":movie['movieicon']

        })
        # 导演
        a = lambda x: "https://movie.douban.com" + x
        auteur = response.xpath("//div[@id='info']/span[1]/span[@class='attrs']/a/text()").extract()
        auteur_ur = response.xpath("//div[@id='info']/span[1]/span[@class='attrs']/a/@href").extract()
        auteur_url = map(a, auteur_ur)
        auteur_info = zip(auteur, auteur_url)

        for info in auteur_info:
            # print(info)
            auterinfo=auteurItem()
            auterinfo['imdb'] = info[1].split("/")[-2]
            auterinfo['name']=info[0]
            auterinfo['url']=info[1]
            # print(auterinfo)
            time.sleep(round(random.uniform(0, 1), 2))
            yield scrapy.Request(url=auterinfo['url'], callback=self.parse_auteur, meta={"item":auterinfo})
            # # 保存导演以及电影
            # # 重启
            movie_au=movie_auteur()
            movie_au['movieid']=movie['movieid']
            movie_au['auteurid']=auterinfo['imdb']
            data={
                "movieid":movie_au['movieid'],
                "auteurid":movie_au['auteurid'],
                "use_db":"movie_auteur"
            }
            print(data)
            # yield data



        # 编剧
        # make = response.xpath("//div[@id='info']/span[2]/span[@class='attrs']/a/text()").extract()
        # make_ur = response.xpath("//div[@id='info']/span[2]/span[@class='attrs']/a/@href").extract()
        # make_url = map(a, make_ur)
        # make_info = zip(make, make_url)
        # print("---------编剧信息------------")
        # for info in make_info:
        #     print(info)
        # 主演
        actor = response.xpath("//div[@id='info']/span[@class='actor']/span[@class='attrs']/a/text()").extract()
        actor_ur = response.xpath("//div[@id='info']/span[@class='actor']/span[@class='attrs']/a/@href").extract()
        actor_url = map(a, actor_ur)
        actor_info = zip(actor, actor_url)
        # print("----------主演信息-------------")
        for info in actor_info:
            actorinfo = actorItem()
            actorinfo['imdb']=info[1].split("/")[-2]
            actorinfo['name'] = info[0]
            actorinfo['url'] = info[1]
            # print(actorinfo)
            time.sleep(round(random.uniform(0, 1), 2))
            yield scrapy.Request(actorinfo['url'], callback=self.parse_actor, meta={"item": actorinfo})
            # 重启
            movie_ac=movie_actor()
            movie_ac['movieid'] = movie['movieid']
            movie_ac['actorid'] = actorinfo['imdb']
            data = {
                "movieid": movie_ac['movieid'] ,
                "actorid":  movie_ac['actorid'],
                "use_db": "movie_actor"
            }
            print(data)
            # yield data

        # 制片国家
        country = response.xpath("//div[@id='info']/span[@class='pl'][./text()='制片国家/地区:']/following::text()[1]").extract()
        # print("制片国家")
        movie['moviecountry']=country
        # 语言
        language = response.xpath("//div[@id='info']/span[@class='pl'][./text()='语言:']/following::text()[1]").extract()
        movie['movielanguage']=language
        # 上映时间
        DataTime = response.xpath("//div[@id='info']/span[@property='v:initialReleaseDate']/text()").extract()
        movie['movieon']=DataTime
        movie['moviedesc']=response.xpath("//span[@property='v:summary']/text()").extract_first().replace("\n","").replace(" ","")
        # print("电影详情页面")
        # # print(item['url'])

        # print(movie)
        data={
            "movie_id":movie['movieid'],
            "name":movie['moviename'],
            "movie_desc":movie['moviedesc'],
            "movie_image":movie['movieicon'],
            "movie_country":";".join(movie['moviecountry']),
            "movie_on":";".join(movie['movieon']),
            "use_db":"moive_info"
        }
        print(data)
        # yield data
        # print("----"*20)
    #导演页面
    def parse_auteur(self,response):
        auteur=response.meta["item"]
        auteur['icon']=response.xpath("//div[@class='item']/div[@class='pic']/a/@href").extract_first()
        infos=response.xpath("//div[@class='info']/ul")
        for info in infos:
                try:
                    # 性别
                    auteur['gender'] = info.xpath("./li/span[./text()='性别']/following::text()[1]").extract_first().replace("\n", "").replace(":",
                                                                                                                      "").replace(
                        " ", "")
                    if len(auteur['gender'])==0:
                        auteur['gender']="保密"
                except:
                    auteur['gender'] = "保密"
                try:
                    dat = re.compile("^[0-9]{2}-[0-9]{2}")
                    # 生日
                    auteur['birth_date'] = info.xpath("./li/span[./text()='出生日期']/following::text()[1]").extract_first().replace("\n", "").replace(":",
                                                                                                                       "").replace(
                        " ", "")
                    if len(auteur['birth_date'])==0:
                        auteur['birth_date']=""
                    if len(auteur['birth_date'])==4:
                        if len(dat.findall(auteur['birth_date']))==1:
                            auteur['birth_date'] = "1900-"+auteur['birth_date']
                        else:
                            auteur['birth_date']=auteur['birth_date']+"-01-01"
                    if len(auteur['birth_date'])>10:
                        auteur['birth_date']=auteur['birth_date'][:10]
                except:
                    auteur['birth_date'] = ""
                try:
                    # 出生地
                    auteur['birth_where'] = info.xpath("./li/span[./text()='出生地']/following::text()[1]").extract_first().replace("\n", "").replace(":",
                                                                                                                      "").replace(
                        " ", "")
                    if len(auteur['birth_where'])==0:
                        auteur['birth_where']=""
                except:
                    auteur['birth_where'] = ""
                try:
                    # 职业
                    auteur['profession'] = info.xpath("./li/span[./text()='职业']/following::text()[1]").extract_first().replace("\n", "").replace(
                        ":", "").replace(" ", "")
                    if len(auteur['profession'])==0:
                        auteur['profession']=""
                except:
                    auteur['profession'] = ""
                data={
                    "imdb":auteur['imdb'],
                    "name":auteur['name'],
                    "gender":auteur['gender'],
                    "birth_where":auteur['birth_where'],
                    "birth_date":auteur['birth_date'],
                    "icon":auteur['icon'],
                    "use_db":"auteur"
                }
                print("导演页面：\n")
                print(data)
                # yield data

                # print(auteur)


    def parse_actor(self,response):
        actor=response.meta["item"]
        actor['icon']=response.xpath("//div[@class='item']/div[@class='pic']/a/@href").extract_first()
        infos=response.xpath("//div[@class='info']/ul")
        for info in infos:
            try:
                actor["gender"] = info.xpath("./li[1]/span/following::text()[1]|a/text()").extract_first().replace("\n", "").replace(":", "").replace(" ", "")
                if len(actor['gender'])==0:
                    actor['gender']="保密"
                actor["birth_date"] = info.xpath("./li[3]/span/following::text()[1]|a/text()").extract_first().replace("\n", "").replace(":", "").replace(" ", "")
                if len(actor['birth_date'])==0:
                    actor['birth_date']=""
                if len(actor['birth_date'])>10:
                    actor['birth_date']=actor['birth_date'][:10]
                actor["birth_where"] = info.xpath("./li[4]/span/following::text()[1]|a/text()").extract_first().replace("\n", "").replace(":", "").replace(" ", "")
                if len(actor['birth_where'])==0:
                    actor['birth_where']=""
                actor["profession"] = info.xpath("./li[5]/span/following::text()[1]|a/text()").extract_first().replace("\n", "").replace(":", "").replace(" ", "")
                if len(actor['profession'])==0:
                    actor['profession']=""
                data = {
                    "imdb": actor['imdb'],
                    "name": actor['name'],
                    "gender": actor['gender'],
                    "birth_where": actor['birth_where'],
                    "birth_date": actor['birth_date'],
                    "icon": actor['icon'],
                    "use_db":"actor"
                }
                print("演员界面")
                print(data)
                # yield data
                # print("演员页面：\n")
                # print(actor)

            except:
                pass
    # def parse_make(self,response):
    #     auteur=response["meta"]
    #     auteur['icon']=response.xpath("//div[@class='pic']/a/@href")
    #     infos=response.xpath("//div[@class='info']/ul")
    #     for info in infos:
    #         auteur["gender"] = info.xpath("./li[1]/span/following::text()[1]|a/text()")[0].replace("\n", "").replace(":", "").replace(" ", "")
    #         auteur["birth_date"] = info.xpath("./li[1]/span/following::text()[1]|a/text()")[0].replace("\n", "").replace(":", "").replace(" ", "")
    #         auteur["birth_where"] = info.xpath("./li[1]/span/following::text()[1]|a/text()")[0].replace("\n", "").replace(":", "").replace(" ", "")
    #         auteur["profession"] = info.xpath("./li[1]/span/following::text()[1]|a/text()")[0].replace("\n", "").replace(":", "").replace(" ", "")
    #         auteur["imdb"] = info.xpath("./li[1]/span/following::text()[1]|a/text()")[0].replace("\n", "").replace(":", "").replace(" ", "")
    #         print("")
    #         print(auteur)
