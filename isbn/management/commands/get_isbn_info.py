from django.core.management.base import BaseCommand
from isbn.models import Book, SearchWord
import requests
import urllib.request
import urllib.parse
import json
from datetime import datetime
import logging
from isbn.utils import get_word_list, create_url, lineNotify

#現在時刻の取得
date_name = datetime.now().strftime("%Y%m%d-%H%M%S")
#ファイル名の生成
file_name = "log" + "\\" + date_name +  "_" + "GET_ISBN_INFO.log"
logging.basicConfig(filename=file_name,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Command(BaseCommand):
    
    """ カスタムコマンド定義 """
        
    def handle(self, *args, **options):
        # ここに実行したい処理を書く
        logging.info('[正常]楽天書籍情報収集処理を開始します。')
        #検索ワードの取得
        word_list = get_word_list()
        for word in word_list:
            # urlを生成
            url = create_url(word)
            # ダウンロード
            req = requests.get(url)
            # json形式で取得
            data = json.loads(req.text)

    def regist_data(data, word):
        for i in range(len(data['Items'])):
            if not Book.objects.filter(isbn=data['Items'][i]['Item']['isbn']).exists():
                #年月日を日付型に変換
                if "日" not in data['Items'][i]['Item']['salesDate']:
                    salesDate = data['Items'][i]['Item']['salesDate'] + "01日"
                    salesDate = salesDate.replace('年','/').replace('月','/').replace('日','')
                    salesDate = datetime.strptime(salesDate, '%Y/%m/%d')
                else:
                    salesDate = data['Items'][i]['Item']['salesDate'].replace('年','/').replace('月','/').replace('日','')
                    salesDate = datetime.strptime(salesDate, '%Y/%m/%d')
        
                #新規登録
                isbn_data = Book.objects.create(
                    word = SearchWord.objects.get(word=word),
                    isbn = data['Items'][i]['Item']['isbn'],
                    salesDate = salesDate,
                    title = data['Items'][i]['Item']['title'],
                    itemPrice = data['Items'][i]['Item']['itemPrice'],
                    imageUrl = data['Items'][i]['Item']['mediumImageUrl'],
                    reviewAverage = data['Items'][i]['Item']['reviewAverage'],
                    reviewCount = data['Items'][i]['Item']['reviewCount'],
                    itemUrl = data['Items'][i]['Item']['itemUrl'],
                    )
                
                #新刊をラインに通知
                message = data['Items'][i]['Item']['itemUrl']
                lineNotify(message)
                    
            #既存エントリーの場合（レビュー数、レビュー平均値の差分だけを更新）
            else:
                #現在のBookレコードを取得
                isbn_data = Book.objects.get(isbn = data['Items'][i]['Item']['isbn'])
                #差分があれば更新
                if data['Items'][i]['Item']['reviewAverage'] != isbn_data.reviewAverage:
                    isbn_data.reviewAverage = data['Items'][i]['Item']['reviewAverage']
                    if data['Items'][i]['Item']['reviewCount'] != isbn_data.reviewCount:
                        isbn_data.reviewCount = data['Items'][i]['Item']['reviewCount']
                                                                
                #反映
                isbn_data.save()
                    
        logging.info('[正常]楽天書籍情報収集処理が正常終了しました。')

