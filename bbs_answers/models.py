from django.db import models
from django.core.validators import MaxLengthValidator

from bbs_questions.models import Question

from module.common import NgWord


# 回答
class Answer(models.Model):

    class Meta:
        db_table = 'bbs_answers'
        verbose_name = '回答'
      
    # 質問ID ※カラム名はquestion_idで生成される
    question = models.ForeignKey(Question, \
        to_field='id', \
        on_delete=models.SET_NULL, null=True, \
        verbose_name='質問ID' )

    # 名前
    name = models.CharField(verbose_name='名前', \
        max_length=50, db_index=True, default='', \
        validators=[MaxLengthValidator(50), NgWord])

    # URL
    url = models.URLField(verbose_name='URL', \
        max_length=250, blank=True, default='', \
        validators=[MaxLengthValidator(250)])

    # 本文
    body = models.TextField(verbose_name='本文', \
        default='', validators=[NgWord])

    # IP
    ip = models.CharField(verbose_name='IP', db_index=True, \
        max_length=100, default='', \
        validators=[MaxLengthValidator(100)])

    # 作成日時     
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新日時 ※管理者モードで弄るので手動
    updated_at = models.DateTimeField()

    def __str__(self):
        return '<id=' + str(self.id) + ', name=' + self.name + '>'


