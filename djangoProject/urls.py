"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from app01.views import depart, user, admin, account, chart, city

urlpatterns = [
    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/detail/', depart.depart_detail),
    path('depart/edit/', depart.depart_edit),
    path('depart/delete/', depart.depart_delete),
    path('depart/multipart/add/', depart.depart_multipart_add),

    # 员工管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/detail/', user.user_detail),
    path('user/edit/', user.user_edit),
    path('user/delete/', user.user_delete),

    # 管理员
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/edit/', admin.admin_edit),
    path('admin/reset/', admin.admin_reset),
    path('admin/delete/', admin.admin_delete),

    # 登录
    path('login/', account.login),
    path('image/code/', account.image_code),
    path('logout/', account.logout),

    # 数据统计
    path('', chart.chart_list),
    path('chart/list/', chart.chart_list),
    path('chart/line/', chart.chart_line),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),

    # 城市列表
    path('city/list/', city.city_list),
    path('city/add/', city.city_add),
    path('city/delete/', city.city_delete),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
]
