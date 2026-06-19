from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('home/', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/zunaira/', views.zp_view, name='zp'),
    path('profile/unaiza/', views.up_view, name='up'),
    path('profile/ahsan/', views.ap_view, name='ap'),
    path('profile/hussain/', views.hp_view, name='hp'),
    path('zunairatools/', views.zunaira_tools_view, name='zunairatools'),
    path('unaizatools/', views.unaiza_tools_view, name='unaizatools'),
    path('ahsantools/', views.ahsan_tools_view, name='ahsantools'),
    path('hussaintools/', views.hussain_tools_view, name='hussaintools'),
    # path('ahsantools/', views.ahsantools, name='ahsantools'),
    # path('hussaintools/', views.hussaintools, name='hussaintools'),
]
