from django.urls import path
from . import views

app_name="administrator"

urlpatterns= [
    path("login/", views.login, name='login'),
    path("logout/",views.logout,name="logout"),
    path("index/",views.index,name="index"),
    path("welcome/",views.welcome,name="welcome"),
    path("order-list/",views.order,name="order_movie"),
    path("search/search_movie/",views.search_moviename,name="search_moviename"),
    path("search/search_actor/",views.search_actorname,name="search_actorname"),
    path("delete_movie/",views.delete_movie,name="delete_movie"),
    path("actor/",views.actor_list,name="actor"),
    path("actor_like/",views.actor_like,name='actor_like'),
    # path("actor/<pindex>",views.actor_list,name="actors"),
    path("actor_add/",views.add_actor,name="add_actor"),
    path("actor_change",views.change_actor,name='change_actor'),
    path("actor_delete/",views.actor_delete,name='actor_delete'),

    path("auteur/",views.auteur_list,name='auteur'),
    path("auteur_like/",views.auteur_like,name='auteur_like'),
    path("auteur_delete/",views.auteur_delete,name='auteur_delete'),
    path("auteur_add/",views.add_auteur,name="add_auteur"),
    path("change_auteur/",views.change_auteur,name="change_auteur"),

    path("search/search_auteur/",views.search_auteurname,name="search_auteurname"),
    path("add-movie/",views.add_movie,name="add_movie"),
    path("change_movie/",views.change_movie,name="change_movie"),
    path("member_list/",views.member_list,name="member_list"),
    path("member_list1/",views.member_list2,name="member_list1"),
    path("member_add/",views.member_add,name="member_add"),
    path("member_similar/",views.member_similar,name="member_del"),
    path("admin_list/",views.admin_list,name="admin_list"),
    path("admin_add/",views.admin_add,name="admin_add"),
    path("admin_chage/",views.admin_chage,name="admin_chage"),
    path("login_log/",views.login_log,name="login_log")


]
