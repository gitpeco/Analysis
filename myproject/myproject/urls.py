from django.contrib import admin
from django.urls import path
from crawler.views import crawler_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/crawler/<str:query>/', crawler_view, name='crawler'),
]