from django.shortcuts import render

from bbs_langtypes.models import LangType

from module.bbs.common import access_counter


def index(request):

    items = LangType.objects.order_by('sort')
   
    # 質問数 コメント数、未返信数、解決数 閲覧数
    sql = (
           'SELECT '
           '   0 as id,' # 主キー用のダミー
           '  (SELECT COUNT(id) FROM bbs_questions ' 
           '     WHERE Z.id = bbs_questions.lang_type_id) AS A,'
           
           '  (SELECT COUNT(bbs_answers.id) FROM bbs_answers  LEFT JOIN '
           '   bbs_questions ON bbs_answers.question_id = bbs_questions.id '
           '   WHERE Z.id = bbs_questions.lang_type_id) AS B, '

           # 未返信数 ※返信がないもの =  1件のみ 
           '  (SELECT'
           '     COUNT(cnt) '
           '   FROM '
           '   ( '
           '   SELECT '
           '    count(question_id) as cnt,bbs_questions.lang_type_id '
           '   FROM '
           '    bbs_answers '
           '   INNER JOIN '
           '    bbs_questions ON bbs_answers.question_id = bbs_questions.id '
           '    GROUP BY question_id   '
           '   HAVING  '
           '     cnt =1  '
           '   ) AS X '
           '  WHERE X.lang_type_id = Z.id) AS C, '
           
           '  (SELECT IFNULL(SUM(CASE WHEN resolved=0 THEN 0 ELSE 1 END),0)'
           '   FROM bbs_questions '
           '   WHERE Z.id = bbs_questions.lang_type_id) AS D, ' 
           
           '  (SELECT IFNULL(SUM(pv),0) FROM '
           '    bbs_questions WHERE Z.id = bbs_questions.lang_type_id) AS E '
           'FROM  '
           '  bbs_lang_types as Z '
           'ORDER BY '
           '  Z.sort ASC')
    counts = LangType.objects.raw(sql)
    
    # QuerySet(items)とRawQuerySet(counts)を結合する
    items = list(items.values())  
    for index, item in enumerate(items):
            
        # 質問数
        item['A'] = counts[index].A
        item['A'] = "{:,}".format(item['A'])
        
        # コメント数
        item['B'] = counts[index].B
        item['B'] = "{:,}".format(item['B'])
                
        # 回答率
        if counts[index].A == 0:
            item['C'] = 0
            item['C'] = "{:,}".format(item['C'])
        else:    
            a = (int(counts[index].A) - int(counts[index].C)) * 1.0
            b = int(counts[index].A)
            item['C'] = round((a / b  * 1.0)  * 100, 2)
            item['C'] = "{:,}".format(item['C']) + '%'
        
        # 解決率
        if counts[index].D == 0:
            item['D'] = 0
            item['D'] = "{:,}".format(item['D'])
        else:    
            a = int(counts[index].D) * 1.0
            b = int(counts[index].A)
            item['D'] = round((a / b * 1.0) * 100, 2)
            item['D'] = "{:,}".format(item['D']) + '%'
            
        # 閲覧数    
        item['E'] = counts[index].E
        item['E'] = "{:,}".format(item['E'])
    
    params ={
        'items': items,
    }
    
    # アクセスカウンター(全体)
    access_counter();
    
    return render(request, 'bbs_main/index.html', params)

