from django.db import models
from django.core.validators import MaxLengthValidator

from bbs_langtypes.models import LangType

from module.common import NgWord


# 質問
class Question(models.Model):

    class Meta:
        db_table = 'bbs_questions'
        verbose_name = '質問'

    # カテゴリID ※カラム名はlang_type_idで生成される
    lang_type = models.ForeignKey(LangType, \
        to_field='id', \
        on_delete=models.SET_NULL, null=True, \
        verbose_name='カテゴリID' )
        
    # タイトル
    title = models.CharField(verbose_name='タイトル', \
        max_length=150, unique=True, default='', \
        validators=[MaxLengthValidator(150), NgWord])

    # 解決
    resolved = models.BooleanField(verbose_name='解決', default=False)

    # PV
    pv = models.IntegerField(verbose_name='PV', default=0)

    # 作成日時     
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新日時 ※管理者モードで弄るので手動
    updated_at = models.DateTimeField()

    def __str__(self):
        return '<id=' + str(self.id) + ', title=' + self.title + '>'


# 検索用(本文)
class Body(models.Model):

    class Meta:
        db_table = 'bbs_bodies'
        verbose_name = '検索用'
    
    # 質問ID ※カラム名はquestion_idで生成される
    question = models.ForeignKey(Question, \
        to_field='id', \
        on_delete=models.SET_NULL, null=True, \
        verbose_name='質問ID' )

    # 検索用(本文のまとめ)
    matome = models.TextField(verbose_name='本文', default='')

    def __str__(self):
        return '<id=' + str(self.id) + ', matome=...>'


