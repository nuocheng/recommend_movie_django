# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql

class DoubanPipeline(object):
    def __init__(self):
        #连接数据库
        self.connect=pymysql.connect(host="127.0.0.1",user="root",passwd="nuocheng",db="movie")
        self.cursor=self.connect.cursor()
        self.f_gender={"女":1,"男":0,"保密":2}
    def process_item(self, item, spider):
        pass
        flag=item['use_db']
        if flag=="actor":
            insert_sql="insert into actor(actor_id,name,gender,birth,place,image) value('{}','{}','{}','{}','{}','{}')".format(item['imdb'],item['name'],self.f_gender[item['gender']],item['birth_date'],item['birth_where'],item['icon'])
            print(insert_sql)
            self.cursor.execute(insert_sql)
            self.connect.commit()


        if flag=="auteur":
            insert_sql=""
            if len(item['birth_date'])==0 and len(item['birth_where'])==0:
                    insert_sql = "insert into auteur(auteur_id,name,gender,image) value('{}','{}','{}','{}')".format(
                    item['imdb'], item['name'], self.f_gender[item['gender']], item['icon'])
            if len(item['birth_where']) != 0 and len(item['birth_date']) == 0:
                    insert_sql = "insert into auteur(auteur_id,name,gender,place,image) value('{}','{}','{}','{}','{}')".format(
                        item['imdb'], item['name'], self.f_gender[item['gender']], item['birth_where'], item['icon'])
            if len(item['birth_where'])==0 and len(item['birth_date'])!=0 :
                insert_sql = "insert into auteur(auteur_id,name,gender,birth,image) value('{}','{}','{}','{}','{}')".format(
                    item['imdb'], item['name'], self.f_gender[item['gender']], item['birth_date'], item['icon'])
            if len(item['birth_where']) != 0 and len(item['birth_date']) != 0:
                insert_sql = "insert into auteur(auteur_id,name,gender,birth,place,image) value('{}','{}','{}','{}','{}','{}')".format(
                    item['imdb'], item['name'], self.f_gender[item['gender']],item['birth_date'], item['birth_where'], item['icon'])
            self.cursor.execute(insert_sql)
            self.connect.commit()
        if flag=="movie":
            insert_sql="insert into movie(movie_id,name,movie_desc,movie_image,movie_country,movie_run) value('{}','{}','{}','{}','{}','{}')".format(item['movieid'],item['moviename'],item['moviedesc'],item['movieicon'],item['moviecountry'],item['movieon'])
            self.cursor.execute(insert_sql)
            self.connect.commit()
        if flag=="movie_auteur":
            insert_sql="insert into movie_movie_auteur(movie_id,auteur_id) value('{}','{}')".format(item['movieid'],item['auteurid'])
            self.cursor.execute(insert_sql)
            self.connect.commit()
        if flag=='movie_actor':
            insert_sql = "insert into movie_movie_actor(movie_id,actor_id) value('{}','{}')".format(item['movieid'],item['actorid'])
            print("\n")
            print(insert_sql)
            self.cursor.execute(insert_sql)
            self.connect.commit()
        if flag=="moive_info":
            insert_sql="insert into movie(movie_id,name,movie_desc,movie_image,movie_country,movie_run) value('{}','{}','{}','{}','{}','{}')".format(item["movie_id"],item["name"],item["movie_desc"],item["movie_image"],item["movie_country"],item["movie_on"])
            print("\n")
            print(insert_sql)
            self.cursor.execute(insert_sql)
            self.connect.commit()
        return item
    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
