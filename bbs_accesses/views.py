from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta 

from django.shortcuts import render

from .models import Access

from module.bbs.common import bbs_login_required


@bbs_login_required
def index(request):
    
    # 現在日時
    today = datetime.today()
    
    # 前月、前年
    month_ago = today + relativedelta(months=-1)
    yyyy_ago = today + relativedelta(years=-1)
     
    # 日毎(1か月分)
    yyyymmdd = month_ago.strftime("%Y") + \
               month_ago.strftime("%m") + \
               month_ago.strftime("%d")

    sql = ( " SELECT 0 as id, yyyy,mm,dd,pv FROM bbs_accesses "
            " WHERE (STR_TO_DATE(yyyy,'%%Y') + STR_TO_DATE(mm,'%%m') "
            "  + STR_TO_DATE(dd,'%%d')) >= %s "
            " ORDER BY yyyy DESC,mm DESC,dd DESC " ) 
    one_month_ago = Access.objects.raw(sql, [yyyymmdd])
    
    # 各月(前年以降)
    sql =( " SELECT  0 as id, yyyy,mm,TRUNCATE(AVG(pv),0) as pv "
           " FROM bbs_accesses"
           " WHERE yyyy >= %s "
           " GROUP BY yyyy,mm "
           " ORDER BY yyyy DESC,mm DESC" ) 
    yyyy = yyyy_ago.strftime("%Y")
    one_year_ago = Access.objects.raw(sql, [yyyy])
    
    # 曜日の追加
    week = ['月','火','水','木','金','土','日']
    for item in one_month_ago:
        d = date(item.yyyy, item.mm, item.dd)
        item.week = week[d.weekday()] 
    
    params ={
        'one_month_ago' : one_month_ago,
        'one_year_ago'  : one_year_ago,
    }
    return render(request, 'bbs_accesses/index.html', params)