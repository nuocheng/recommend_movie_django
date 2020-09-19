from django.db import models

# 电影类型
class movie_type(models.Model):
    id=models.AutoField("电影类型编号",primary_key=True)
    name=models.CharField("电影类型",max_length=50,null=False,blank=False)
    class Meta:
        db_table="movie_type"

#导演信息
class auteur(models.Model):
    auteur_id=models.CharField(primary_key=True,max_length=30,null=False,blank=False,default="00000")
    name=models.CharField("导演名称",max_length=225,null=False,blank=False)
    gender=models.IntegerField(choices=((0,"男"),(1,"女"),(2,"男")),default=2)
    birth=models.DateField(null=True,blank=True)
    place=models.CharField("出生地",max_length=225,null=True,blank=True)
    graduation = models.CharField("毕业学校", max_length=225, null=True, blank=True)
    image=models.ImageField("头像",upload_to="icon/%Y%m%d")
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    class Meta:
        db_table="auteur"

#演员
class actor(models.Model):
    actor_id = models.CharField(primary_key=True,max_length=30,null=False,blank=False,default="00000")
    name=models.CharField("演员名字",max_length=60,null=False,blank=False)
    gender=models.IntegerField("性别",choices=((0,"男"),(1,"女"),(2,"保密")),default=2)
    birth = models.DateField(null=True,blank=True)
    place=models.CharField("出生地",max_length=225,null=True,blank=True)
    graduation=models.CharField("毕业学校",max_length=225,null=True,blank=True)
    image=models.ImageField("头像",upload_to="icon/%Y%m%d")
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    class Meta:
        db_table="actor"

#电影
class movie(models.Model):
    movie_id = models.CharField(primary_key=True,max_length=30,null=False,blank=False,default="00000")
    name=models.CharField("电影名称",max_length=225,null=True,blank=True)
    movie_type=models.ManyToManyField(movie_type)
    movie_desc=models.TextField("简介")
    movie_image=models.ImageField("电影宣传页",upload_to="movie/%Y%m%d")
    movie_auteur=models.ManyToManyField(auteur,related_name="movie_auteur")
    movie_actor=models.ManyToManyField(actor,related_name="movie_actor")
    movie_country=models.CharField("电影拍摄国家",max_length=225,null=True,blank=True)
    movie_run=models.CharField("电影上映时间",null=True,blank=True,max_length=225)
    movie_score=models.FloatField("电影评分",default="0.0")
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table="movie"


class user_info(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=225)
    password=models.CharField(max_length=225)

    class Meta:
        db_table="user_info"

class score(models.Model):
    user_id=models.ForeignKey(user_info,on_delete=models.CASCADE,related_name="userid")
    movie_id=models.ForeignKey(movie,on_delete=models.CASCADE,related_name="movieid")
    score=models.IntegerField()

    class Meta:
        db_table="score"

class admin_info(models.Model):
    id=models.AutoField(primary_key=True)
    adminname=models.CharField(max_length=225)
    password=models.CharField(max_length=225)

    class Meta:
        db_table="admin_info"