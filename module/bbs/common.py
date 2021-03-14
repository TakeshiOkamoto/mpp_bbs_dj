# ------------------
#  固有の共通処理
# ------------------
from datetime import datetime

from django.db import transaction
from django.shortcuts import redirect

from bbs_accesses.models import Access
from bbs_questions.models import Body
from bbs_answers.models import Answer


# ログインのリダイレクト用 ※デコレータ(@)
def bbs_login_required (function):
    def actual_decorator(*args, **kwargs):
        request = args[0]
        if not 'name' in request.session:
            return redirect('bbs_main:index')
        return function(*args, **kwargs)
    return actual_decorator


# (検索用)本文テーブルの更新
def body_table_update(question_id, isDeleteOnly):
    
    # 本文を削除
    items = Body.objects.filter(question_id=question_id)
    if items.count() != 0:
        item = Body.objects.get(id=items[0].id)
        with transaction.atomic(): 
            item.delete()
    
    # 検索用の本文を最新の状態にする 
    if isDeleteOnly == False:
        answers = Answer.objects.filter(question_id=question_id)
        matome = ''
        for answer in answers:
            matome = matome + ' ' + answer.body
            
        item = Body()
        item.question_id = question_id
        item.matome = matome
        with transaction.atomic(): 
            item.save()


# アクセスカウンター(全体)
def access_counter():
    yyyy = datetime.now().strftime("%Y")
    mm = datetime.now().strftime("%m")
    dd = datetime.now().strftime("%d")
    
    # 新規
    items = Access.objects.filter(yyyy=yyyy, mm=mm, dd=dd)
    if items.count() == 0:
        item = Access()
        item.yyyy = yyyy
        item.mm = mm
        item.dd = dd
        item.pv = 1
        with transaction.atomic(): 
            item.save()
    # 更新        
    else:
        item = Access.objects.get(id=items[0].id)
        item.pv = item.pv +1
        with transaction.atomic(): 
            item.save()


