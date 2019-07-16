import pandas as pd
import requests
from lxml import html
import json
import numpy

# 종목이름으로 부터 종목 코드 받아오기
# 데이터는 krx .....
class Krx:

    data_file = "data/market_stock_item_data.csv"

    def get_stock_code_by_name(self, stock_name):
        file = open(self.data_file, "rt", encoding="utf8")

        for line in file.readlines():
            token = line.split(",")
            code = token[1]
            name = token[2]

            if stock_name == name:
                return code

    def get_all_stock_items(self):
        file = open(self.data_file, "rt", encoding="utf8")

        stock_item_list = []
        for line in file.readlines():
            token = line.split(",")
            code = token[1]
            name = token[2]
            data = (code, name)
            stock_item_list.append(data)

        stock_item_list = stock_item_list[1:]

        return stock_item_list

    def get_short(self, krx_code):
        url = "https://short.krx.co.kr/contents/COM/GenerateOTP.jspx?bld=SRT/02/02010100/srt02010100X&name=form"
        otp = requests.get(url).content

        url = "https://short.krx.co.kr/contents/SRT/99/SRT99000001.jspx"
        parameters = {"isu_cd": krx_code, "strt_dd": "20190605","end_dd": "20190705", "code": otp}
        data = requests.post(url, parameters).content.decode("utf-8")
        #print(data)

        json_data = json.loads(data)['block1']

        print("공매도거래량, 공매도거래대금")
        for data in json_data:
            print(data['cvsrtsell_trdvol'] + "          " + data['cvsrtsell_trdval'])


class Fnguide:

    pre_url = "http://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN=&gicode=A"

    def get_per(self, code):
        url = self.pre_url + code
        page = requests.get(url)
        tree = html.fromstring(page.content)

        elements = tree.xpath("//div[@id=\"corp_group2\"]/dl/dd")
        per = elements[2].text
        return per

    def get_sales_profit_by_stock_code(self, code):
        url = self.pre_url + code
        result = pd.read_html(url)

        df = None
        for page in result:
            if 'GAAP(연결)' in page.columns or 'IFRS(연결)' in page.columns:
                df = page

        if df is None:
            return None

        df.columns = df.columns.droplevel()

        if 'GAAP(연결)' in df.columns:
            df = df.set_index('GAAP(연결)')
        else:
            df = df.set_index('IFRS(연결)')


        df = df.loc['영업이익']

        index_2018 = None

        for index in df.index:
            if "2018" in index:
                index_2018 = index

        if index_2018 is None:
            return None

        sales_profit = df[index_2018]

        if type(sales_profit) is numpy.float64 or type(sales_profit) is float or type(sales_profit) is str:
            return sales_profit
        else:
            return sales_profit.values[0]


stock_name = "삼성전자"
krx = Krx()
fnguide = Fnguide()

'''
10 페이지 Krx에서 전종목 받아오는 코드
#code = krx.get_stock_code_by_name(stock_name)
#sales_profit = fnguide.get_sales_profit_by_stock_code(code)
#print(stock_name + "," + str(sales_profit))
'''

#11 페이지 pandas로 데이터 프레임 얻어서 영업이익 구하기, lxml 을 이용해 per 구하기
stock_item_list = krx.get_all_stock_items()
print("종목명,영업이익,per")
for stock_item in stock_item_list:
    code = stock_item[0]
    name = stock_item[1]
    sales_profit = fnguide.get_sales_profit_by_stock_code(code)
    per = fnguide.get_per(code)
    print(name + "," + str(sales_profit) + "," + per)


# 13 패이지 일별 공매도량 구하는 코드
# krx.get_short("KR7005930003")