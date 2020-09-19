import math
import json
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect,reverse
from django.core.paginator import Paginator , PageNotAnInteger,EmptyPage
from administrator.models import movie,actor,auteur,user_info,score
# Create your views here.recommend

def index(request):
    userid=request.session.get("userid")
    username=request.session.get("username")
    movie_last=movie.objects.all().order_by("create_at")
    movie_good_score=movie.objects.all().order_by("movie_score")
    movies=movie.objects.all().order_by("-create_at")
    movie_count=movie.objects.all().count()
    actor_count=actor.objects.all().count()
    auteur_count=auteur.objects.all().count()
    if userid is None or username is None:
        print("进入未登录界面")
        context={
            "flag":0,#表示未登录
            "page2": list(movie_last)[0:14],
            "page2_2": list(movie_last)[14:29],
            "page2_3": list(movie_last)[29:40],
            "page3": list(movie_good_score)[0:14],
            "page3_2": list(movie_good_score)[14:27],
            "page4":list(movies)[0:14],
            "page4_2": list(movies)[14:25],
            "movie_count": movie_count,
            "actor_count": actor_count,
            "auteur_count": auteur_count
        }
        return render(request,'home/index.html',context=context)
    else:
        print("进入登录界面")
        user_see_count=score.objects.filter(user_id=userid).count()
        # print(user_see_count)
        persion_comment=[]
        if user_see_count != 0:
            get_all_user_score()
            simial_persion = recommend(userid)
            # print(simial_persion)
            movie_id = score.objects.filter(user_id=int(simial_persion)).values("movie_id")
            for m in list(movie_id):
                pc = movie.objects.get(pk=m['movie_id'])
                persion_comment.append(pc)
            context={
                "flag": 1,  # 表示登录
                "page1":persion_comment,
                 "page2": list(movie_last)[0:14],
                "page2_2": list(movie_last)[14:29],
                "page2_3": list(movie_last)[29:40],
                "page3": list(movie_good_score)[0:14],
                "page3_2": list(movie_good_score)[14:27],
                "page4":list(movies)[0:14],
                "page4_2": list(movies)[14:25],
                "movie_count": movie_count,
                "actor_count": actor_count,
                "auteur_count": auteur_count,
                "username": username,
                "userid": userid,
            }
            return render(request, 'home/index.html', context=context)
        else:
            print("进入新用户")
            context = {
                "flag": 2,  # 表示登录
                "page1":None,
                "page2": list(movie_last)[0:14],
                "page2_2": list(movie_last)[14:29],
                "page2_3": list(movie_last)[29:40],
                "page3": list(movie_good_score)[0:14],
                "page3_2": list(movie_good_score)[14:27],
                "page4":list(movies)[0:14],
                "page4_2": list(movies)[14:25],
                "movie_count": movie_count,
                "actor_count": actor_count,
                "auteur_count": auteur_count,
                "username": username,
                "userid": userid,
            }
            return render(request, 'home/index.html', context=context)






def search(request):
    username = request.session.get("username")
    userid = request.session.get("userid")
    context = {
        "username": username,
        "userid": userid,
    }
    return render(request,"home/search.html",context=context)

def movie_info(request):
    keyword=request.GET.get("keyword")
    #使用跨app使用models
    movies=type(movie())
    datas = []
    infos = movies.objects.filter(name__icontains=keyword)
    for info in infos:
        data={
            "name": info.name
        }
        # data = {
        #     "movie_id": info.movie_id,
        #     "name": info.name,
        #     "movie_desc": info.movie_desc,
        #     "movie_image": str(info.movie_image),
        #     "movie_country": info.movie_country,
        #     "movie_run": info.movie_run,
        #     "create_at": info.create_at,
        #     "actor": list(info.movie_actor.all().values()),
        #     "auteur": list(info.movie_auteur.all().values()),
        #     "message": 1
        # }
        datas.append(data)
    return JsonResponse(datas, safe=False)

#查询列表页
def movie_desc(request):
    username = request.session.get("username")
    userid = request.session.get("userid")
    keyword=request.GET.get("keyword")
    movies=type(movie())
    datas=[]
    infos=movies.objects.filter(name__icontains=keyword)
    for info in infos:
        data={
            "movie":info.movie_id,
            "name":info.name,
            "movie_desc":info.movie_desc,
            "movie_image":str(info.movie_image),
            "movie_country":info.movie_country,
            "movie_run":info.movie_run,
            "create_at":info.create_at,
            "actor":list(info.movie_actor.values("actor_id","name")),
            "auteur":list(info.movie_auteur.values("auteur_id","name")),
        }
        datas.append(data)
    pindex=request.GET.get("pindex")
    pageinator=Paginator(datas,5)
    if pindex=="" or pindex==None:
        pindex=1
    page=pageinator.page(pindex)
    context={
        "keyword":keyword,
        "data":page,
        "username":username,
        "userid":userid
    }
    return render(request,"home/search.html",context=context)


#用户评分电影
def movie_score(request):
    return render(request,"home/score_system.html")

#用户评分数据
def score_save(request):
    if request.method=="POST":
        userid=int(request.POST.get("user_id"))
        movie_id=request.POST.get("movie_id")
        sc=request.POST.get("movie_score")
        #获得用户
        user=user_info.objects.filter(pk=userid).first()
        #获得电影
        movie_d=movie.objects.filter(movie_id=movie_id).first()
        # 判断用户是否已经对电影进行评分，是的话就进行数据更新即可
        way_add=score.objects.filter(user_id=user,movie_id=movie_d)
        if way_add.count()==1:
            way_add.score=sc
            flag=1
            return JsonResponse({"data": flag}, safe=False)
        else:
            score_sys=score()
            score_sys.user_id=user
            score_sys.movie_id=movie_d
            score_sys.score=sc
            print(sc)
            score_sys.save()
            flag=2
            return JsonResponse({"data": flag}, safe=False)



#登录页面
def login(request):
    if request.method=="GET":
        return render(request,"home/login.html")
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        info=user_info.objects.filter(username=username,password=password)
        if len(info)==0:
            context={
                "message":"用户不存在，请检查您的输入是否正确"
            }
            return render(request,"home/login.html",context=context)
        else:
            request.session['userid'] = info.first().id
            request.session["username"]=info.first().username
            return redirect(reverse("home:index"))
#注册页面
def register(request):
    if request.method=="GET":
        print("进入get")
        return render(request,"home/register.html")
    if request.method=="POST":
        print("进入post")
        username=request.POST.get("username")
        password=request.POST.get("password")
        print({
            "username":username,
            "password":password
        })
        user=user_info()
        user.username=username
        user.password=password
        user.save()
        #用户注册完直接跳转到登录页面
        return redirect(reverse("home:login"))

# #退出登录操作
def logout(request):
    userid = request.session.get("userid")
    username = request.session.get("username")
    if userid is None and username is None:
        request.session.flush()
        return redirect(reverse("home:index"))
    else:
        print("跳转")
        return redirect(reverse("home:login"))


#推荐系统部分
#获取全部用户的评分
def get_all_user_score():
    data_values=list(score.objects.all().values("user_id_id","movie_id_id","score"))
    global user_item
    data=pd.DataFrame(data_values)
    # print(data)
    user_item=data.pivot(index='user_id_id',columns='movie_id_id',values='score')

#向量
def build_xy(user_id1,user_id2):
    bool_array = user_item.loc[user_id1].notnull() & user_item.loc[user_id2].notnull()
    return user_item.loc[user_id1, bool_array], user_item.loc[user_id2, bool_array]

# 皮尔逊相关系数
def pearson(user_id1, user_id2):
    x, y = build_xy(user_id1, user_id2)
    mean1, mean2 = x.mean(), y.mean()
    # 分母
    denominator = (sum((x-mean1)**2)*sum((y-mean2)**2))**0.5
    try:
        value = sum((x - mean1) * (y - mean2)) / denominator
    except ZeroDivisionError:
        value = 0
    # print(str(user_id1)+"与"+str(user_id2)+"的相似度为"+str(value))
    return value

# 获取前三个相似度高的矩阵
def computeNearestNeighbor(user_id, k=3):
    return user_item.drop(user_id).index.to_series().apply(pearson, args=(user_id,)).nlargest(k)


#推荐返回
def recommend(user_id):
    # 找到最相似的用户id
    nearest_user_id = computeNearestNeighbor(user_id).index[0]
    # print('最相似用户ID：')
    # print(nearest_user_id)
    # return user_item.loc[nearest_user_id, user_item.loc[user_id].isnull() & user_item.loc[nearest_user_id].notnull()].sort_values()
    return nearest_user_id

