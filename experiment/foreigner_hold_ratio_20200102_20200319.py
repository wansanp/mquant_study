
from raw_data_access.Krx import Krx
import requests
import ast

krx = Krx()

stock_item_list = krx.get_all_stock_item_list()

print("종목명,2020-01-02 외인보유 량, 2020-01-02 외인보유 비율, 2020-03-19 외인보유 량, 2020-03-19 외인보유 비율")

for stock_item in stock_item_list:

    try:
        res = requests.get('https://m.stock.naver.com/api/item/getTrendList.nhn?size=54&bizdate=20200320&code='+stock_item[0])
        result = ast.literal_eval(res.text)['result']

        last_status = result[0]
        first_status = result[-1]

        last_foreign_hold_ratio = str(last_status['frgn_hold_ratio'])
        last_foreign_hold_quantity = str(last_status['frgn_stock'])

        first_foreign_hold_ratio = str(first_status['frgn_hold_ratio'])
        first_foreign_hold_quantity = str(first_status['frgn_stock'])

        print(stock_item[1] + "," + first_foreign_hold_quantity + "," + first_foreign_hold_ratio + "," + last_foreign_hold_quantity + "," + last_foreign_hold_ratio)
    except KeyError:
        None
