from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.utils.http import urlencode
from django.core.paginator import Paginator

from .models import LangType
from .forms import LangTypeForm, FindForm

from module.common import trim
from module.bbs.common import bbs_login_required


@bbs_login_required
def index(request):
    
    # 検索
    items = LangType.objects.all()
    if 'name' in request.GET:
    
        # フォームの生成
        name = trim(request.GET['name'])
        data = {
            'name' : name,
        }    
        form = FindForm(data)

        # 複数キーワード
        if name != '':
            arr = name.split(' ')
            for val in arr:
                if val != '':
                    items = items.filter(name__icontains=val)
        
        # 検索用
        search_param = '&' + urlencode({'name': name})
    else:
        form = FindForm() 
        search_param = ''
    items = items.order_by('sort')
    
    # ページネーション 
    per_page = 10 # ページ毎に表示するアイテム数
    paginator = Paginator(items, per_page)
    if 'page' in request.GET: 
        if request.GET['page'].isdecimal():
            current_page = int(request.GET['page'])
            items = paginator.get_page(current_page)
        else:
            return redirect(to='bbs_lang_types:index')
    else:
        current_page = 1
        items = paginator.get_page(current_page)

    if items.paginator.count > 0:
        message ='全%s件中 %s - %s件のデータが表示されています。' % \
           ( items.paginator.count, \
              ( current_page -1) * per_page + 1, \
              ((current_page -1) * per_page + 1)  + \
               (len(items) -1) \
           )
    else:
        message = 'データがありません。'
    
    params = {
        'form': form,
        'items': items,
        'message' : message,
        'search_param': search_param,
    }    
    return render(request, 'bbs_langtypes/index.html', params)


@bbs_login_required
def create(request):

    params = {}
    if (request.method == 'POST'):

        # モデルフォームの生成
        data ={
            'name'        : trim(request.POST['name']),
            'keywords'    : trim(request.POST['keywords']),
            'description' : trim(request.POST['description']),
            'sort' : request.POST['sort'],
            'show' : request.POST['show'] if 'show' in request.POST \
                            else False,
        }
        lang_type = LangTypeForm(data)
        
        # バリデーション
        if (lang_type.is_valid()):
        
            # トランザクション
            try:
                with transaction.atomic(): 
                    lang_type.save()
                    messages.success(request, "登録しました。")
            except Exception as e:
                messages.error(request, \
                    "エラーが発生しました。管理者に問い合わせてください。")
                
            return redirect(to='bbs_lang_types:index')

        else:
            params['form'] = lang_type
            messages.error(request, "エラーをご確認ください。")
    else:    
        params['form'] = LangTypeForm()
        
    return render(request, 'bbs_langtypes/create.html', params)


@bbs_login_required
def show(request, id):

    item = LangType.objects.get(id=id)
    params = {
        'item': item,
    }    
    return render(request, 'bbs_langtypes/show.html', params)


@bbs_login_required
def edit(request, id):
    
    item = LangType.objects.get(id=id)
    params = {
        'id': id,
    }

    if (request.method == 'POST'):

        # モデルフォームの生成
        data ={
            'name'        : trim(request.POST['name']),
            'keywords'    : trim(request.POST['keywords']),
            'description' : trim(request.POST['description']),
            'sort' : request.POST['sort'],
            'show' : request.POST['show'] if 'show' in request.POST \
                        else False,
        }    
        lang_type = LangTypeForm(data, instance=item)
        
        # バリデーション
        if (lang_type.is_valid()):
        
            # トランザクション
            try:
                with transaction.atomic(): 
                    lang_type.save()
                    messages.success(request, "更新しました。")
            except Exception as e:
                messages.error(request, \
                    "エラーが発生しました。管理者に問い合わせてください。")
                
            return redirect(to='bbs_lang_types:index')
            
        else:
            params['form'] = lang_type
            messages.error(request, "エラーをご確認ください。")
    else:        
        params['form'] = LangTypeForm(instance=item)
    
    return render(request, 'bbs_langtypes/edit.html', params)


@bbs_login_required
def delete(request, id):

    lang_type = LangType.objects.get(id=id)
    if (request.method == 'DELETE'):
    
        # トランザクション
        try:
            with transaction.atomic(): 
                lang_type.delete()
                messages.error(request, "削除しました。")
        except Exception as e:
            messages.error(request, \
                "エラーが発生しました。管理者に問い合わせてください。")
    return HttpResponse('')


