"""mpp_bbs_dj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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

urlpatterns = [
    
    # この管理ツール(admin)は本番では削除して下さい。
    path('admin/', admin.site.urls),
    
    path('', include('bbs_main.urls')),    
    path('questions/', include('bbs_questions.urls')),
    path('answers/', include('bbs_answers.urls')),
    path('lang_types/', include('bbs_langtypes.urls')),
    path('accesses/', include('bbs_accesses.urls')),
    path('login/', include('bbs_login.urls')),
]
