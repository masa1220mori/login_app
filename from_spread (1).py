#!/home/iriiida/anaconda3/bin/python3
# -- coding: utf-8 --
import gspread
import json
import numpy as np

#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet-####.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY1 = '###'
SPREADSHEET_KEY2 = '###'

workbook_member = gc.open_by_key(SPREADSHEET_KEY1)
workbook_result = gc.open_by_key(SPREADSHEET_KEY2)
#共有設定したスプレッドシートのシート1を開く
worksheet_member = workbook_member.sheet1
worksheet_result_jun = workbook_result.worksheet('2019/06月')
worksheet_result_july = workbook_result.worksheet('2019/07月')
news = workbook_result.sheet1

class Get_spread():
        name_list=np.asarray(worksheet_member.col_values(3))
        result_july=np.asarray(worksheet_result_july.get_all_values(), dtype="<U")

class ZerotenNews():
        news=np.asarray(news.get_all_values(), dtype="<U")