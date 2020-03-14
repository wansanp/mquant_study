
from raw_data_access.Krx import Krx
from raw_data_access.Naver import Naver
import requests
import ast

krx = Krx()
naver = Naver()

def code_to_isin(name):
    parameters = {
        'method': 'searchCorpNameJson',
        'searchCorpName': name,
        'spotIsuTrdMktTpCd': '1',
        'comAttrTpCd': '1'
    }

    res = requests.post('https://kind.krx.co.kr/common/searchcorpname.do', parameters)
    result = ast.literal_eval(res.text)[0]
    isin_code = result['repisucd']
    return isin_code


stock_item_list = krx.get_all_stock_item_list()

for stock_item in stock_item_list:

    day_count = 19

    stock_day_price_list = naver.get_all_data_by_code(stock_item[0], day_count)
    isin_code = code_to_isin(stock_item[0])
    short_volume_dict = krx.get_short_stock_selling(isin_code, '2020/02/18', '2020/03/13')

    total_ratio = 0

    for stock_day_price in stock_day_price_list:

        try:
            #날짜,시가,고가,저가,종가,거래량
            token = stock_day_price.split("|")
            date = token[0]
            volume = token[5].replace(",", "")
            #  : 공매도 거래량, #  : 공매도 잔고량, #  : 공매도 거래대금 ,#  : 공매도 잔고금액
            short_volume = short_volume_dict[date]
            ratio = int(short_volume[0].replace(",", "")) / int(volume)
            total_ratio += ratio

        except ZeroDivisionError:
            day_count -= 1
        except KeyError:
            day_count -= 1

    try:
        total_ratio = round(total_ratio / day_count, 4)
    except ZeroDivisionError:
        total_ratio = 0.0

    print(stock_item[1] + "," + str(total_ratio))
