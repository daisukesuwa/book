from isbn.models import Book, SearchWord
import urllib.parse
import requests
from datetime import datetime

def get_word_list():
    
    #検索ワードリストの生成
    word_list =[]
    queryset = SearchWord.objects.all().filter(flag=True)
    for item in queryset:
        word_list.append(item.word)
    return word_list

def create_url(word):
    
    #検索ワードに登録されているワードの書籍情報を検索
    API = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
    APPLICATION_ID = "自分のDIを記載する"

    values = {
        "applicationId": APPLICATION_ID,
        "format": "json",  # 出力形式
        "title": word
            }
    #パラメータのエンコード処理
    params = urllib.parse.urlencode(values)
    # リクエスト用のURLを生成
    url = API + "?" + params
    return url

def lineNotify(message):
    line_notify_token = 'iitMvdx4A1lFlNKP8bpnxOO0PZbZ7Tsq6wcjpObSLWV'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    requests.post(line_notify_api, data=payload, headers=headers)


