import numpy as np
import pandas as pd
import time
from django.shortcuts import render,redirect
from .models import *
import json
from django.http import JsonResponse,HttpResponse,HttpRequest
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.shortcuts import reverse,redirect
from .models import movie,actor,auteur,admin_info,user_info

# Create your views here.
def login(request):
    if request.method=='GET':
        return render(request,"administrator/login.html")
    if request.method=='POST':
        username=request.POST.get("name")
        password=request.POST.get("password")
        # print(username)
        admincount=admin_info.objects.filter(adminname=username,password=password).values("id","adminname","password")
        if admincount.count()==1:
            request.session['adminname']=username
            request.session['password']=password
            print(list(admincount)[0]['id'])
            request.session['id']=list(admincount)[0]['id']

        return JsonResponse({"exist_count":admincount.count()})

def logout(request):
    request.session.flush()
    return redirect(reverse("administrator:login"))

def index(request):
    adminname=request.session.get("adminname")
    password=request.session.get("password")
    # print(adminname)
    if adminname is not None:
        context={
            "adminname":adminname,
            "password":password
        }
        print(context)
        return render(request,"administrator/index.html",context=context)
    else:
        return redirect(reverse("administrator:login"))



#欢迎页面
def welcome(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        movie_count=movie.objects.all().count()   #电影的数量
        actor_count=actor.objects.all().count()   #演员的数量
        user_count=user_info.objects.all().count() #用户数量
        admin_count=admin_info.objects.all().count()#管理员数量
        data_list,count_list=echart_data()
        context={
            "movie_count":movie_count,
            "user_count":user_count,
            "admin_count":admin_count,
            "data_list":json.dumps(data_list),
            "count_list":str(count_list)
        }
        print(str(data_list))
        return render(request,"administrator/welcome.html",context=context)
    else:
        return redirect(reverse("administrator:login"))

#电影列表界面
def order(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        #查询数据中中所有的啊电影信息
        datas=[]
        movies=movie.objects.all()
        for movie_info in movies:
            actors=list(movie_info.movie_actor.all().values("name"))
            auteur=list(movie_info.movie_auteur.all().values("name"))

            info={
                "movie_id":movie_info.movie_id,
                "name":movie_info.name,
                "movie_image":str(movie_info.movie_image),
                "movie_country":movie_info.movie_country,
                "movie_actor":actors,
                "movie_auteur":auteur,
                "create_at":movie_info.create_at,
                "update_at":movie_info.update_at
            }
            datas.append(info)
        paginator = Paginator(datas, 10,2)
        page = request.GET.get('page',"1")
        try:
            current_page = paginator.page(page)
            # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            current_page = paginator.page(1)
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            books = paginator.page(paginator.num_pages)
        context={
            "datas":current_page,
            'paginator': paginator
        }
        return render(request,"administrator/order-list.html",context=context)
    else:
        return redirect(reverse("administrator:login"))

#电影查询
def search_moviename(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='POST':
            keyword=request.POST.get("movie_name")
            print(keyword)
            datas=[]
            movies=movie.objects.filter(name__icontains=keyword)
            for movie_info in movies:
                actors = list(movie_info.movie_actor.all().values("name"))
                auteur = list(movie_info.movie_auteur.all().values("name"))

                info = {
                    "movie_id": movie_info.movie_id,
                    "name": movie_info.name,
                    "movie_image": str(movie_info.movie_image),
                    "movie_country": movie_info.movie_country,
                    "movie_actor": actors,
                    "movie_auteur": auteur,
                    "create_at": movie_info.create_at,
                    "update_at": movie_info.update_at
                }
                datas.append(info)
            paginator = Paginator(datas, 10, 2)
            page = request.GET.get('page', "1")
            try:
                current_page = paginator.page(page)
                # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                current_page = paginator.page(1)
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                books = paginator.page(paginator.num_pages)
            context = {
                "datas": current_page,
                'paginator': paginator
            }
            return render(request, "administrator/order-list.html", context=context)
    else:
        return redirect(reverse("administrator:login"))



#演员查询
def search_actorname(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='POST':
            keyword=request.POST.get("movie_name")
            datas=[]
            actors_info=actor.objects.filter(name__icontains=keyword)
            for ac in actors_info:
                movies=ac.movie_actor.all()
                for movie_info in movies:
                    actors = list(movie_info.movie_actor.all().values("name"))
                    auteur = list(movie_info.movie_auteur.all().values("name"))
                    info = {
                        "movie_id": movie_info.movie_id,
                        "name": movie_info.name,
                        "movie_image": str(movie_info.movie_image),
                        "movie_country": movie_info.movie_country,
                        "movie_actor": actors,
                        "movie_auteur": auteur,
                        "create_at": movie_info.create_at,
                        "update_at": movie_info.update_at
                    }
                    datas.append(info)
            paginator = Paginator(datas, 10, 2)
            page = request.GET.get('page', "1")
            try:
                current_page = paginator.page(page)
                # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                current_page = paginator.page(1)
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                books = paginator.page(paginator.num_pages)
            context = {
                "datas": current_page,
                'paginator': paginator
            }
            return render(request, "administrator/order-list.html", context=context)
    else:
        return redirect(reverse("administrator:login"))

#演员列表
def actor_list(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='GET':
            actorlist=list(actor.objects.all().values("actor_id","name","gender","birth","place","image"))
            paginator = Paginator(actorlist, 15)

            page = request.GET.get('page')
            try:
                info = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                info = paginator.page(1)
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                info = paginator.page(paginator.num_pages)
            context={
                "info":info,
            }
            print(context)
            # print(context)
            return render(request,'administrator/actor.html',context=context)
    else:
        return redirect(reverse("administrator:login"))

#演员列表的模糊查询
def actor_like(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='GET':
            keyword=request.GET.get("keyword")
            page = request.GET.get('page')

            actorlist=list(actor.objects.filter(name__icontains=keyword).values("actor_id","name","gender","birth","place","image"))
            paginator = Paginator(actorlist, 10)

            try:
                info = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                info = paginator.page(1)
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                info = paginator.page(paginator.num_pages)
            context = {
                "info": info,
                "keyword":keyword
            }
            print(context)
            # print(context)
            return render(request, 'administrator/actor_search.html', context=context)
    else:
        return redirect(reverse("administrator:login"))



#演员添加
def add_actor(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='GET':
            context = {
                "flag": 1  # 2表示添加的意思
            }
            return render(request,'administrator/actor-add.html',context=context)
        elif request.method=='POST':
            name=request.POST.get("name")
            gender=request.POST.get('gender')
            birth=request.POST.get('birth')
            place=request.POST.get("place")
            image=request.FILES.get("file")
            a_info =actor()
            a_info.actor_id = int(time.time() * 10)
            a_info.name = name
            a_info.gender = gender
            a_info.birth = birth
            a_info.place = place
            a_info.image = image
            a_info.save()
            response_data = {"info": "操作成功"}
            return JsonResponse(response_data,safe=False)
    else:
        return redirect(reverse("administrator:login"))

#演员的修改
def change_actor(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='GET':
            id=request.GET.get("userid")
            actor_info=actor.objects.filter(actor_id=id)
            context={
                "info":list(actor_info)[0],
                "flag":2   #2表示修改的意思
            }
            print(context)
            return render(request,'administrator/actor-add.html',context=context)
        if request.method=='POST':

            actor_id=request.POST.get("actor_id")
            name = request.POST.get("name")
            gender = request.POST.get('gender')
            birth = request.POST.get('birth')
            place = request.POST.get("place")
            image = request.FILES.get("file")
            a_i=actor.objects.filter(actor_id=actor_id).first()
            print("进入演员修改页面")
            # print(list(a_i))
            a_i.name=name
            a_i.gender=gender
            a_i.birth=birth
            a_i.place=place
            if image != None:
                a_i.image=image
            a_i.save()
            response_data = {"info": "操作成功"}
            return JsonResponse(response_data)

    else:
        return redirect(reverse("administrator:login"))


#演员的删除
def actor_delete(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='GET':
            id=request.GET.get("userid")
            print(id)
            actor_info=actor.objects.filter(actor_id=id)
            print(actor_info)
            actor_info.delete()
            return JsonResponse({"data":1},safe=False)
    else:
        return redirect(reverse("administrator:login"))

#导演查询
def search_auteurname(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='POST':
            keyword = request.POST.get("movie_name")
            datas = []
            auteur_info = auteur.objects.filter(name__icontains=keyword)
            for au in auteur_info:
                movies = au.movie_auteur.all()
                for movie_info in movies:
                    actors = list(movie_info.movie_actor.all().values("name"))
                    auteurs = list(movie_info.movie_auteur.all().values("name"))
                    info = {
                        "movie_id": movie_info.movie_id,
                        "name": movie_info.name,
                        "movie_image": str(movie_info.movie_image),
                        "movie_country": movie_info.movie_country,
                        "movie_actor": actors,
                        "movie_auteur": auteurs,
                        "create_at": movie_info.create_at,
                        "update_at": movie_info.update_at
                    }
                    datas.append(info)
            paginator = Paginator(datas, 10, 2)
            page = request.GET.get('page', "1")
            try:
                current_page = paginator.page(page)
                # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                current_page = paginator.page(1)
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                books = paginator.page(paginator.num_pages)
            context = {
                "datas": current_page,
                'paginator': paginator
            }
            return render(request, "administrator/order-list.html", context=context)
    else:
        return redirect(reverse("administrator:login"))

#导演列表
def auteur_list(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='GET':
            actorlist=list(auteur.objects.all().values("auteur_id","name","gender","birth","place","image"))
            paginator = Paginator(actorlist, 15)

            page = request.GET.get('page')
            try:
                info = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                info = paginator.page(1)
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                info = paginator.page(paginator.num_pages)
            context={
                "info":info,
            }
            print(context)
            # print(context)
            return render(request,'administrator/auteur.html',context=context)
    else:
        return redirect(reverse("administrator:login"))

#导演列表的模糊查询
def auteur_like(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='GET':
            keyword=request.GET.get("keyword")
            page = request.GET.get('page')

            actorlist=list(auteur.objects.filter(name__icontains=keyword).values("auteur_id","name","gender","birth","place","image"))
            paginator = Paginator(actorlist, 10)

            try:
                info = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                info = paginator.page(1)
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                info = paginator.page(paginator.num_pages)
            context = {
                "info": info,
                "keyword":keyword
            }
            print(context)
            # print(context)
            return render(request, 'administrator/auteur_search.html', context=context)
    else:
        return redirect(reverse("administrator:login"))

#导演的删除
def auteur_delete(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='GET':
            id=request.GET.get("userid")
            print(id+"\n")
            actor_info=auteur.objects.filter(auteur_id=id).first()
            print(actor_info)
            actor_info.delete()
            return JsonResponse({"data":1})
    else:
        return redirect(reverse("administrator:login"))
#导演添加
def add_auteur(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='GET':
            context = {
                "flag": 1  # 2表示添加的意思
            }
            return render(request,'administrator/auteur-add.html',context=context)
        elif request.method=='POST':
            name=request.POST.get("name")
            gender=request.POST.get('gender')
            birth=request.POST.get('birth')
            place=request.POST.get("place")
            image=request.FILES.get("file")
            a_info=auteur()
            a_info.auteur_id=int(time.time()*10)
            a_info.name=name
            a_info.gender=gender
            a_info.birth=birth
            a_info.place=place
            a_info.image=image
            a_info.save()
            response_data={"info":"操作成功"}
            return JsonResponse(response_data,safe=False)
    else:
        return redirect(reverse("administrator:login"))
#电影添加界面
def add_movie(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        return render(request,"administrator/order-add.html")
    else:
        return redirect(reverse("administrator:login"))
#电影修改页
def change_movie(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        return render(request,"administrator/order-view.html")
    else:
        return redirect(reverse("administrator:login"))

#电影删除页面
def delete_movie(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='GET':
            movie_id=request.GET.get("movie_id")
            movie_d=movie.objects.filter(movie_id=movie_id)
            flag=0
            success=0
            if movie_d.count()==0:
                flag=0   #表示没有
            else:
                flag=1   #表示存在
                success=1
                movie_d.delete()
            context={
                "flag":flag,
                "success":success
            }
            return JsonResponse(context)

    else:
        return redirect(reverse("administrator:login"))

#导演的修改
def change_auteur(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='GET':
            id=request.GET.get("userid")
            actor_info=auteur.objects.filter(auteur_id=id)
            context={
                "info":list(actor_info)[0],
                "flag":2   #2表示修改的意思
            }
            print(context)
            return render(request,'administrator/auteur-add.html',context=context)
        if request.method=='POST':
            auteur_id = request.POST.get("actor_id")
            name = request.POST.get("name")
            gender = request.POST.get('gender')
            birth = request.POST.get('birth')
            place = request.POST.get("place")
            image = request.FILES.get("file")
            a_i = auteur.objects.filter(auteur_id=auteur_id).first()
            print("进入导演修改页面")
            # print(list(a_i))
            a_i.name = name
            a_i.gender = gender
            a_i.birth = birth
            a_i.place = place
            if image != None:
                a_i.image = image
            a_i.save()
            response_data = {"info": "操作成功"}
            return JsonResponse(response_data)

    else:
        return redirect(reverse("administrator:login"))
#用户管理界面
def statstic_people(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        return render(request,"administrator/")
    else:
        return redirect(reverse("administrator:login"))

#用户列表
def member_list(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        userlist=list(user_info.objects.all().values())
        people_info = []
        for user_i in userlist:
            userid=user_i['id']
            user_looked_list=list(score.objects.filter(user_id=userid).values("movie_id"))
            movie_ns=[]
            # print(user_looked_list)
            for moiveid in user_looked_list:
                moviename=list(movie.objects.filter(movie_id=moiveid['movie_id']).values("name"))[0]['name']
                movie_ns.append(moviename)
            info={
                "user_base":user_i,
                "looked_movie":movie_ns
            }
            people_info.append(info)
        context={
            "infos":people_info
        }
        return render(request,"administrator/member-list.html",context=context)
    else:
        return redirect(reverse("administrator:login"))

#用户列表2
def member_list2(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        return render(request,"administrator/member-list1.html")
    else:
        return redirect(reverse("administrator:login"))
#用户添加页面
def member_add(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        return render(request,"administrator/member-add.html")
    else:
        return redirect(reverse("administrator:login"))

#用户相似度对比问题
def member_similar(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        get_all_user_score()
        userid_list=user_info.objects.all().values("id")
        # print(list(userid_list))
        similar_information=[]
        for user_id in list(userid_list):
            # 用户相似列表，最相似的用户id，推荐的电影
            # print(user_id['id'])
            try:
                similar_dict,similar_id,movie_list=recommend(user_id['id'])

                echarts_data1=json.loads(similar_dict).keys()
                echarts_data2=json.loads(similar_dict).values()

                people_name=user_info.objects.filter(id=similar_id).values("username")
                s_m_id=list(score.objects.filter(user_id=similar_id).values("movie_id"))
                people_l_m=[]
                for movie_id in s_m_id:
                    m_n=list(movie.objects.filter(movie_id=movie_id['movie_id']).values("name"))[0]['name']
                    # print(m_n)
                    people_l_m.append(m_n)
                movie_id=list(movie_list.keys())[-1]
                movie_score=list(movie_list.values())[-1]
                movie_info=movie.objects.filter(movie_id=movie_id).values("movie_image","name","movie_desc").first()
                info={
                    "userid":user_id['id'],
                    "desc":json.loads(similar_dict),
                    "echarts_data1":list(echarts_data1),
                    "echarts_data2":list(echarts_data2),
                    "people_name":list(people_name)[0],
                     "people_looked_moive":people_l_m,
                    "movie_scroe":movie_score,
                    "movie_info":movie_info
                }
                similar_information.append(info)
            except:
                #出现错误的id
                print("出现错误的id"+str(user_id['id']))
        context={
            "similar_information":similar_information

        }
        # print(similar_information[0])
        return render(request, "administrator/member-similar.html",context=context)
    else:
        return redirect(reverse("administrator:login"))


#管理员列表
def admin_list(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        id=request.session.get("id")
        print(adminname)
        print(id)
        print(id)
        print(id)
        adminlist=list(admin_info.objects.all())
        context={
            "id":id,
            "infos":adminlist
        }
        return render(request,"administrator/admin-list.html",context=context)
    else:
        return redirect(reverse("administrator:login"))
#管理员添加界面
def admin_add(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='GET':
            return render(request,"administrator/admin-add.html")
        elif request.method=='POST':
            name=request.POST.get("name")
            password=request.POST.get("pass")
            add_admin=admin_info()
            add_admin.adminname=name
            add_admin.password=password
            add_admin.save()
            return JsonResponse({"success":1})
    else:
        return redirect(reverse("administrator:login"))
#管理员修改界面
def admin_chage(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        if request.method=='GET':
            admininfo=admin_info.objects.filter(pk=request.session.get("id")).values("id","adminname","password")
            context={
                "info":list(admininfo)[0]
            }
            return render(request,"administrator/admin-edit.html",context=context)
        if request.method=='POST':
            id=request.POST.get("id")
            name = request.POST.get("name")
            password = request.POST.get("pass")
            add_admin = admin_info.objects.get(pk=id)
            add_admin.adminname = name
            add_admin.password = password
            add_admin.save()
            return JsonResponse({"success": 1})
    else:
        return redirect(reverse("administrator:login"))

#登录记录：
def login_log(request):
    adminname = request.session.get("adminname")
    password = request.session.get("password")
    if adminname is not None:
        return render(request,"administrator/log.html")
    else:
        return redirect(reverse("administrator:login"))




#数据分析部分
#按照时间段进行可视化展示
def echart_data():
    movie_list=movie.objects.all().values("create_at")
    movie_info = []
    movie_data = pd.DataFrame(list(movie_list))
    # print(movie_data)
    data_group = pd.to_datetime(movie_data['create_at'])

    # 开始按照年，计算每一年上传的数量
    data_years = data_group.dt.year
    info = data_years.value_counts()
    year_list = info.to_dict()
    # 根据年内的数据
    # print(year_list)
    for demo in year_list:
        years = demo
        # 某一年下的月的数量信息
        information = {}

        month_group = data_group.loc[data_group.dt.year == demo]
        month_info = month_group.dt.month.value_counts().to_dict()
        # print(month_info)
        for m in month_info:
            # 某月下的信息量

            day_grop = month_group.loc[month_group.dt.month == m]
            day_info = day_grop.dt.day.value_counts().to_dict()
            # print(day_info)
            # 某日下的信息量
            for d in day_info:

                hour_group = day_grop.loc[day_grop.dt.day == d]
                hour_info = hour_group.dt.hour.value_counts().to_dict()
                # print(hour_info)
                # 某时下的数据量
                for h in hour_info:

                    minute_group = hour_group.loc[hour_group.dt.hour == h]
                    # print(minute_group)
                    minute_info = minute_group.dt.minute.value_counts().to_dict()
                    # print(minute_info)
                    for mi in minute_info:
                        info = {
                            "time": str(years) + "-" + str(m) + "-" + str(d) + " " + str(h) + ":" + str(mi),
                            "count": minute_info[mi]
                        }
                        movie_info.append(info)

    # print(movie_info)
    movie_df = pd.DataFrame(movie_info)
    # print(movie_df)
    # print(movie_df['time'].sort_values(ascending=True).tolist())
    # print(movie_df['count'].sort_values(ascending=True).tolist())
    return movie_df['time'].sort_values(ascending=True).tolist(),movie_df['count'].sort_values(ascending=False).tolist()



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
    return round(value,2)

# 计算最相似的邻居
def computeNearestNeighbor(user_id):
    # print(json.dumps(user_item.drop(user_id).index.to_series().apply(pearson, args=(user_id,)).to_dict()))
    return json.dumps(user_item.drop(user_id).index.to_series().apply(pearson, args=(user_id,)).to_dict()),user_item.drop(user_id).index.to_series().apply(pearson, args=(user_id,)).nlargest(1).index[0]


#用户相似列表，最相似的用户id，推荐的电影
def recommend(user_id):
    #用户的相似比,以及相似度最高的用户id
    user_similar,most_similar=computeNearestNeighbor(user_id)
    movie_list=user_item.loc[most_similar, user_item.loc[user_id].isnull() & user_item.loc[most_similar].notnull()].sort_values().to_dict()
    return user_similar,most_similar,movie_list

