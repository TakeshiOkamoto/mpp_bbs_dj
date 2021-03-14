from django import forms
from .models import LangType


# カテゴリのモデルフォーム
class LangTypeForm(forms.ModelForm):
    class Meta:
        model = LangType
        fields = ['name', 'keywords', 'description', 'sort', 'show']


# 検索フォーム
class FindForm(forms.Form):
    name = forms.CharField(initial='')