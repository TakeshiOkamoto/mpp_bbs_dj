from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from .models import User

from module.common import trim


def login(request):

    if (request.method == 'POST'):
        email = trim(request.POST['email'])
        password = trim(request.POST['password'])

        # バリデーション
        users = User.objects.filter(email=email)
        if users.count() == 1:
            if check_password(password, users[0].password):
                request.session['name']  = users[0].name 
                request.session['email'] = users[0].email
                messages.success(request, "ログインしました。")
                return redirect('bbs_main:index') 
                            
        messages.error(request, \
                "メールアドレスまたはパスワードが一致しません。")
        return redirect('bbs_login:login') 
    return render(request, 'bbs_login/index.html') 

def loguot(request):
    if 'name' in request.session:
        del request.session['name']
    if 'email' in request.session:
        del request.session['email']
    return redirect('bbs_main:index')


