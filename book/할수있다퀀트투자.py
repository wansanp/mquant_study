import pandas as pd
from raw_data_access.Krx import Krx
from raw_data_access.Fnguide import Fnguide

def chapter8_035():

    krx = Krx()
    fnguide = Fnguide()

    stock_item_list = krx.get_all_stock_item_list()

    for stock_item in stock_item_list:
        code = stock_item[0]
        df = fnguide.get_fnguide_financial_dataframe(code)
        if df is None:
            print(stock_item[1])

    #df = pd.DataFrame(columns=("종목명", "PSR"))
    #df = df.append({"종목명": "삼성전자", "PSR": 31111}, ignore_index=True)

    #df.to_csv("../result/result.csv")


chapter8_035()