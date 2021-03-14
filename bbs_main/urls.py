from django.urls import path
from . import views


app_name = 'bbs_main'

urlpatterns = [
   path('', views.index, name='index'),
]