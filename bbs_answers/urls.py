from django.urls import path
from . import views


app_name = 'bbs_answers'

urlpatterns = [
   path('', views.index, name='index'),
   path('edit/<int:id>', views.edit, name='edit'),
   path('delete/<int:id>', views.delete, name='delete'),
]