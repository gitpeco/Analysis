from django.contrib import admin
from django.urls import path, include
from main import views  # 导入主应用的视图
from django.urls import path
from . import views
from urllib.parse import quote
app_name = 'main'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('search/', views.search, name='search'),
    path('', views.login, name='index'),  # 将根路径映射到登录视图
]