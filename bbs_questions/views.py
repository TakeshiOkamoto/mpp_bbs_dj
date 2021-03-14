from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.utils.http import urlencode
from django.core.paginator import Paginator
from django.utils import timezone
    
from .models import Question
from .models import Body
from bbs_langtypes.models import LangType
from bbs_questions.models import Question
from bbs_answers.models import Answer

from .forms import FindForm
from .forms import QuestionForm
from .forms import AnswerForm

from module.common import trim, url, get_ip_address
from module.bbs.common import access_counter, body_table_update
from module.bbs.common import bbs_login_required


def index(request):

    # 不正対策
    if 'lang_id' in request.GET: 
        if request.GET['lang_id'].isdecimal():
            lang_id = int(request.GET['lang_id'])
        else:
            return redirect(to='bbs_main:index')
    else:
        return redirect(to='bbs_main:index')

    lang_types = LangType.objects.filter(id=lang_id)
    if lang_types.count() == 0:
        return redirect(to='bbs_main:index')
        
    # 検索(LEFT JOIN)
    items = Body.objects.select_related('question') \
                .filter(question__lang_type_id=lang_id)
        
    title = ''
    if 'title' in request.GET:
         title = trim(request.GET['title'])
    body = ''
    if 'body' in request.GET:
         body = trim(request.GET['body'])
    
    search_param = '&' + urlencode({'lang_id': lang_id})
    if title != '':
        search_param = '&' + urlencode({'title': title})
    if body != '':
        search_param = '&' + urlencode({'body': body})
        
    data = {
        'title' : title,
        'body'  : body,
    }    
    form = FindForm(data)
    
    # WHERE(タイトル)
    if title != '':
        arr = title.split(' ')
        for val in arr:
            if val != '':
                items = items.filter(question__title__icontains=val)
    # WHERE(本文)
    if body != '':
        arr = body.split(' ')
        for val in arr:
            if val != '':
                items = items.filter(matome__icontains=val)
    
    # ORDER BY(DESC)
    items = items.order_by('question__updated_at').reverse()
    
    # 質問者、最終発言者、件数の配列を取得する
    params = dict(lang_type_id=lang_id)
    sql =(
        ' SELECT '
        '   bbs_questions.id,'
        '  (SELECT bbs_answers.name FROM bbs_answers ' 
        '   WHERE  bbs_answers.question_id = bbs_questions.id '
        '   ORDER BY bbs_answers.id ASC LIMIT 1) as name1,'
        '  (SELECT bbs_answers.name FROM bbs_answers'
        '   WHERE bbs_answers.question_id = bbs_questions.id '
        '   ORDER BY bbs_answers.id DESC LIMIT 1) as name2,'
        '  (SELECT count(id) FROM bbs_answers '
        '   WHERE bbs_answers.question_id = bbs_questions.id) as cnt '
        ' FROM bbs_questions  '
        ' WHERE '
        '  bbs_questions.lang_type_id = %(lang_type_id)s'
        ' ORDER BY'
        '  bbs_questions.updated_at DESC'
        % params)
    db_data = Question.objects.raw(sql)

    # ページネーション 
    per_page = 25 # ページ毎に表示するアイテム数
    paginator = Paginator(items, per_page)
    if 'page' in request.GET: 
        if request.GET['page'].isdecimal():
            current_page = int(request.GET['page'])
            items = paginator.get_page(current_page)
        else:
            return redirect(to=url('bbs_questions:index', lang_id=lang_id))
    else:
        current_page = 1
        items = paginator.get_page(current_page)

    if items.paginator.count > 0:
        message ='全%s件中 %s - %s件の質問が表示されています。' % \
           ( items.paginator.count, \
              ( current_page -1) * per_page + 1, \
              ((current_page -1) * per_page + 1)  + \
               (len(items) -1) \
           )
    else:
        message = '質問がありません。'

    # django.core.paginator.Page(items)とRawQuerySet(db_data)を結合する
    for item in items:
        cnt = '破損'
        name1 = ''
        name2 = ''
        for obj in db_data:
            if obj.id == item.question.id:
                if obj.cnt != '':
                    cnt = "{:,}".format(obj.cnt)
                if obj.name1 != None:
                    name1 = obj.name1
                if obj.name2 != None:
                    name2 = obj.name2
                break
                
        # メンバ編集        
        item.id = item.question.id
        item.pv = "{:,}".format(item.question.pv)
        item.updated_at = item.question.updated_at
        item.cnt = cnt
        item.name1 = name1
        item.name2 = name2
    
    params = {
        'form': form,
        'items': items,
        'message' : message,
        'lang_type' : lang_types[0],
        'search_param': search_param,
    }    

    # アクセスカウンター(全体)
    access_counter()
    
    return render(request, 'bbs_questions/index.html', params)


def create(request):
    
    # 不正対策
    if 'lang_id' in request.GET: 
        if request.GET['lang_id'].isdecimal():
            lang_id = int(request.GET['lang_id'])
        else:
            return redirect(to='bbs_main:index')
    else:
        return redirect(to='bbs_main:index')

    lang_types = LangType.objects.filter(id=lang_id)
    if lang_types.count() == 0:
        return redirect(to='bbs_main:index')
    
    # メイン処理
    params = {
      'lang_type' : lang_types[0],
    }

    if (request.method == 'POST'):

        # モデルフォーム(質問)の生成
        data ={
            'lang_type'  : lang_id,
            'title'      : trim(request.POST['title']),
            'resolved'   : False,
            'pv'         : 1,
            'updated_at' : timezone.now(),
        }        
        question = QuestionForm(data)
        
        # モデルフォーム(回答)の生成
        data ={
            'name'       : trim(request.POST['name']),
            'url'        : trim(request.POST['url']),
            'body'       : trim(request.POST['body']),
            'ip'         : get_ip_address(request),
            'updated_at' : timezone.now(),
        }        
        answer = AnswerForm(data)
                
        # バリデーション
        if (question.is_valid() and answer.is_valid()):
        
            # トランザクション
            try:
                with transaction.atomic(): 
                
                    # 質問
                    question = question.save()
                    question.updated_at = question.created_at
                    question.save()

                    # 回答
                    # ※フォームで除外されているquestionは2回目で更新する
                    answer = answer.save()
                    answer.question = question
                    answer.save()

                    # (検索用)本文テーブルの更新
                    body_table_update(question.id, False)
                    
                    messages.success(request, "登録しました。")
            except Exception as e:
                messages.error(request, \
                    "エラーが発生しました。管理者に問い合わせてください。" +e)
                    
            return redirect(url('bbs_questions:index', lang_id=lang_id))

        else:
            params['form_A'] = question
            params['form_B'] = answer
            messages.error(request, "エラーをご確認ください。")
    else:    
        params['form_A'] = QuestionForm()
        params['form_B'] = AnswerForm()

    return render(request, 'bbs_questions/create.html', params)


@bbs_login_required
def delete(request, id):

    question =  Question.objects.get(id=id)
    if (request.method == 'DELETE'):
    
        # トランザクション
        try:
            with transaction.atomic(): 
                # 関連も全て削除する
                answers = Answer.objects.filter(question_id=question.id)
                for answer in answers:
                    answer.delete()
                body_table_update(question.id, True)
                question.delete()
                messages.error(request, "削除しました。")
        except Exception as e:
            messages.error(request, \
                "エラーが発生しました。管理者に問い合わせてください。")
    return HttpResponse('')


