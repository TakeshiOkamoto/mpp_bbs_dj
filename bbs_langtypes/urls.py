from django.urls import path
from . import views


app_name = 'bbs_lang_types'

urlpatterns = [
   path('', views.index, name='index'),
   path('create', views.create, name='create'),
   path('show/<int:id>', views.show, name='show'), 
   path('edit/<int:id>', views.edit, name='edit'),
   path('delete/<int:id>', views.delete, name='delete'),
]