"""
URL configuration for mydjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include

from graphene_django.views import GraphQLView

from data_process.views import trigger_task, check_default_task, check_default_progress
from data_process.views import add_book
from mydjango.schema import schema


urlpatterns = [
    path("admin/", admin.site.urls),

    path('django-rq/', include('django_rq.urls')),  # Django RQ dashboard
    path('trigger/', trigger_task),
    path('check_rq/<str:rq_id>', check_default_task),
    path('check_rq_progress/<str:rq_id>', check_default_progress),

    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
    # http://localhost:8000/graphql/
    # 新增graphql統一入口
    # 如果在 GraphQLView 中没有特别指定 schema 參數，會使用 settings.py 裡預設的 GRAPHENE
    path('add_book/', add_book),
]
