from django import forms
from .models import Question
from bbs_answers.models import Answer


# 質問フォーム
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['lang_type', 'title', 'resolved', 'pv', 'updated_at']


# 回答フォーム
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['name', 'url', 'body', 'ip', 'updated_at']


# 検索フォーム
class FindForm(forms.Form):
    title = forms.CharField(initial='')
    body = forms.CharField(initial='')