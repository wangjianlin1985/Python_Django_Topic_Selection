"""PythonProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.views.static import serve #需要导入
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),#这部分很重要
    url(r'^ClassInfo/', include('apps.ClassInfo.urls', namespace='ClassInfo')),  # 班级信息模块
    url(r'^UserInfo/', include('apps.UserInfo.urls', namespace='UserInfo')),  # 学生信息模块
    url(r'^Teacher/', include('apps.Teacher.urls', namespace='Teacher')),  # 教师信息模块
    url(r'^Subject/', include('apps.Subject.urls', namespace='Subject')),  # 题目信息模块
    url(r'^SubjectType/', include('apps.SubjectType.urls', namespace='SubjectType')),  # 题目类型模块
    url(r'^SelectItem/', include('apps.SelectItem.urls', namespace='SelectItem')),  # 学生选题模块
    url(r'^Leaveword/', include('apps.Leaveword.urls', namespace='Leaveword')),  # 留言模块
    url(r'^Notice/', include('apps.Notice.urls', namespace='Notice')),  # 新闻公告模块

    url(r'^', include("apps.Index.urls", namespace="Index")),  # 首页模块

    url(r'^tinymce/', include('tinymce.urls')),
]
