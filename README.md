# 掲示板システム
  
DEMO    
[https://www.petitmonte.com/django/bbs/](https://www.petitmonte.com/django/bbs/)  
  
[mpp_bbs_djの意味]  
mpp = My Practice Project  
bbs = 掲示板  
dj = Django   
    
## 1. 環境
・Django 3.2系  
・MariaDB 10.2.2以上 (MySQL5.5以上でも可)  
 
## 2. インストール方法

### Djangoのバージョン
Django 3.2系です。
```rb
python -m pip install Django==3.2.*
```

最新の3.2系は2021年4月公開予定です。公開前は[開発版(ベータなど)](https://code.djangoproject.com/wiki/Version3.2Roadmap)  をインストール可能です。
```rb
pip install --pre django
```
### 必要なPythonパッケージ
```rb
pip install python-dateutil 
```
※日付及び時刻操作で使用しています。
### settings.py
< データベース >
```rb
DATABASES = {
    'default': {        
        # ココのデータベース設定を行う
        'NAME': 'データベース名',
        'USER': 'ユーザー名',
        'PASSWORD': 'パスワード',
        }        
    }
}
```
< SECRET_KEY >  
本番稼働する際はSECRET_KEYを再生成して下さい。
```rb
cd プロジェクトディレクトリ
python manage.py shell
```
シェルが起動したら次のコードを実行します。  
```rb
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
exit()
```
表示された値をSECRET_KEYに設定します。  

### マイグレーション
```rb
cd プロジェクトディレクトリ
python manage.py migrate
```
### 管理者アカウントの作成
次のコマンドを実行する。
```rb
cd プロジェクトディレクトリ
python manage.py shell
```
シェルが起動したら次のコードを実行します。  
※name、email、passwordの値は任意です。
```rb
from django.contrib.auth.hashers import make_password
from bbs_login.models import User

user = User()
user.name = 'admin'
user.email = 'admin@example.com'
user.password = make_password('12345678')
user.save()

exit()
```


### 実行する
```rb
python manage.py runserver
```
メイン    
[http://localhost:8000/](http://localhost:8000/)   
ログイン   
[http://localhost:8000/login/](http://localhost:8000/login/) 
  
## 3. Djangoプロジェクトの各種初期設定
その他は次の記事を参照してください。  
  
[Djangoプロジェクトの各種初期設定](https://www.petitmonte.com/python/django_project.html)  

## 同梱ファイルのライセンス
Bootstrap v4.3.1 (https://getbootstrap.com/)  
```rb
Copyright 2011-2019 The Bootstrap Authors  
Copyright 2011-2019 Twitter, Inc.
```

