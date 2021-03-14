from django.db import models


# アクセス
class Access(models.Model):

    class Meta:
        db_table = 'bbs_accesses'
        verbose_name = 'アクセス'

    # 年
    yyyy = models.IntegerField(verbose_name='年', \
        db_index=True)

    # 月
    mm = models.IntegerField(verbose_name='月', \
        db_index=True)

    # 日
    dd = models.IntegerField(verbose_name='日', \
        db_index=True)

    # PV
    pv = models.IntegerField(verbose_name='PV')

    # 作成日時
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<id=' + str(self.id) + ', ' + \
             str(self.yyyy) + '/' + str(self.mm) + '/' + str(self.dd)  + '>'
