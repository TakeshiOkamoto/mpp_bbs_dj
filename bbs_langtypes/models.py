from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.validators import MinValueValidator, MaxValueValidator


# カテゴリ
class LangType(models.Model):

    class Meta:
        db_table = 'bbs_lang_types'
        verbose_name = 'カテゴリ'
        
    # 名前
    name = models.CharField(verbose_name='名前', \
        max_length=50, unique=True, default='', \
        validators=[MaxLengthValidator(50)])
    
    # キーワード  
    keywords = models.CharField(verbose_name='キーワード', \
        max_length=100, default='', \
        validators=[MaxLengthValidator(100)])
    
    # 説明  
    description = models.TextField(verbose_name='説明', \
        max_length=512, blank=True, default='', \
        validators=[MaxLengthValidator(512)])
    
    # ソート
    sort = models.IntegerField(verbose_name='ソート', \
        validators=[ \
            MinValueValidator(0), \
            MaxValueValidator(1000)])
    
    # 表示
    show = models.BooleanField(verbose_name='表示', default=True)

    # 作成日時     
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<id=' + str(self.id) + ', name=' + self.name + '>'
