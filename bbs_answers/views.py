from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone

from .models import Answer
from bbs_questions.models import Question
from bbs_questions.models import Body
from bbs_langtypes.models import LangType

from bbs_questions.forms import AnswerForm

from module.common import trim, url, get_ip_address
from module.bbs.common import access_counter, body_table_update
from module.bbs.common import bbs_login_required


def index(request):
    
    # 不正対策
    if 'question_id' in request.GET: 
        if request.GET['question_id'].isdecimal():
            question_id = int(request.GET['question_id'])
        else:
            return redirect(to='bbs_main:index')
    else:
        return redirect(to='bbs_main:index')

    questions = Question.objects.filter(id=question_id)
    if questions.count() == 0:
        return redirect(to='bbs_main:index')
    lang_types = LangType.objects.filter(id=questions[0].lang_type_id)
    if lang_types.count() == 0:
        return redirect(to='bbs_main:index')
    items = Answer.objects.filter(question_id=questions[0].id) \
            .order_by('updated_at')
   
    # タイトル毎の閲覧数の更新
    question = Question.objects.get(id=questions[0].id)
    question.pv = question.pv + 1
    with transaction.atomic(): 
        question.save()

    # アクセスカウンター(全体)
    access_counter()
    
    # メイン処理
    params = {
      'items'     : items,
      'lang_type' : lang_types[0],
    }
    if (request.method == 'POST'):
        
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
        if (answer.is_valid()):
        
            # トランザクション
            try:
                with transaction.atomic(): 

                    # 回答
                    # ※フォームで除外されているquestionは2回目で更新する
                    answer = answer.save()
                    answer.question = question
                    answer.save()
                    
                    # (検索用)本文テーブルの更新
                    body_table_update(question.id, False)
                                        
                    # 質問 
                    if 'resolved' in request.POST:
                        question.resolved = True
                    question.updated_at = answer.updated_at
                    question.save()
                    
                    messages.success(request, "返信しました。")
            except Exception as e:
                messages.error(request, \
                    "エラーが発生しました。管理者に問い合わせてください。" +e)
                    
            return redirect(url('bbs_answers:index', question_id=question.id))

        else:
            params['form'] = answer
            messages.error(request, "エラーをご確認ください。")
    else:    
        params['form'] = AnswerForm()
    
    params['question'] = question
    return render(request, 'bbs_answers/index.html', params)


@bbs_login_required
def edit(request, id):

    answer = Answer.objects.get(id=id)
    question = Question.objects.get(id=answer.question.id)

    # メイン処理
    params = {
      'answer'   : answer,
      'question' : question,
    }
    if (request.method == 'POST'):
        
        # モデルフォーム(回答)の生成
        data ={
            'name'       : trim(request.POST['name']),
            'url'        : trim(request.POST['url']),
            'body'       : trim(request.POST['body']),
            'ip'         : answer.ip,
            'updated_at' : answer.updated_at,
        }        
        answer = AnswerForm(data, instance=answer)
              
        if 'resolved' in request.POST:
            question.resolved = True
        else:
            question.resolved = False
            
        # バリデーション
        if (answer.is_valid()):
        
            # トランザクション
            try:
                with transaction.atomic(): 

                    # 回答
                    # ※フォームで除外されているquestionは2回目で更新する
                    answer = answer.save()
                    answer.question = question
                    answer.save()
                    
                    # (検索用)本文テーブルの更新
                    body_table_update(question.id, False)

                    # 質問
                    question.save()
                    
                    messages.success(request, "更新しました。")
            except Exception as e:
                messages.error(request, \
                    "エラーが発生しました。管理者に問い合わせてください。" +e)
                    
            return redirect(url('bbs_answers:index', question_id=question.id))

        else:
            params['form'] = answer
            messages.error(request, "エラーをご確認ください。")
    else:    
        params['form'] = AnswerForm(instance=answer)
        
    params['question'] = question
    return render(request, 'bbs_answers/edit.html', params)


@bbs_login_required
def delete(request, id):
    
    answer = Answer.objects.get(id=id)
    question = Question.objects.get(id=answer.question.id)
    if (request.method == 'DELETE'):
    
        # トランザクション
        try:
            with transaction.atomic(): 
                answer.delete()
                answers = Answer.objects.filter(question_id=question.id) \
                            .order_by('updated_at').reverse()
                if answers.count() == 0:
                    body = Body.objects.get(question_id=question.id)
                    body.matome = ''
                    body.save()
                else:
                    body_table_update(question.id, False)
                    question.updated_at = answers[0].updated_at
                    question.save()
                messages.error(request, "削除しました。")
        except Exception as e:
            messages.error(request, \
                "エラーが発生しました。管理者に問い合わせてください。" + e)
    return HttpResponse('')


