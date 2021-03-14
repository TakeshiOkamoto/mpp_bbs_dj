from django.urls import path
from . import views


app_name = 'bbs_accesses'

urlpatterns = [
   path('', views.index, name='index'),
]