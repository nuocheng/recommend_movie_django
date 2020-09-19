from django.urls import path
from . import views
app_name="home"

urlpatterns=[
    path("",views.index,name="index"),
    path("search/",views.search,name='search'),
    path("movie_info/",views.movie_info,name='movie_info'),
    path("moive_search/",views.movie_desc,name='movie_desc'),
    path("movie_socre/",views.movie_score,name="movie_score"),
    path("login/",views.login,name="login"),
    path("add-score/",views.score_save,name="score_save"),
    path("register/",views.register,name="register"),
    path("logout/",views.logout,name="logout")
]