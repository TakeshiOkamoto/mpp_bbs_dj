from django.urls import path
from . import views


app_name = 'bbs_login'

urlpatterns = [
   path('', views.login, name='login'),
   path('out/', views.loguot, name='loguot'),
]