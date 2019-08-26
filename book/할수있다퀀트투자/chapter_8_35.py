from raw_data_access.Krx import Krx
from raw_data_access.Fnguide import Fnguide
from raw_data_access.Naver import Naver
from raw_data_process.Sise import Sise
import math
import numpy as np

def chapter8_035():

    krx = Krx()
    fnguide = Fnguide()
    sise = Sise()
    naver = Naver()

    stock_item_list = krx.get_all_stock_item_list()

    print("종목명,시가총액,매출액,PSR,상승률,상승하락,년초가,현재가,결산월")

    for stock_item in stock_item_list:

        code = stock_item[0]
        df = fnguide.get_fnguide_financial_dataframe(code)
        if df is None:
            continue

        if 'IFRS(연결)' not in df.columns or 'Annual' not in df.columns:
            print(stock_item[1] + ",n/a")
            continue

        df = df[['IFRS(연결)', 'Annual']]

        df.columns = df.columns.droplevel()
        df = df.set_index('IFRS(연결)')

        year_settlement = None

        if '2019/03' in df.columns:
            year_settlement = '2019/03'
        elif '2018/06' in df.columns:
            year_settlement = '2018/06'
        elif '2019/02' in df.columns:
            year_settlement = '2019/02'
        elif '2019/01' in df.columns:
            year_settlement = '2019/01'
        elif '2018/07' in df.columns:
            year_settlement = '2018/07'
        elif '2018/09' in df.columns:
            year_settlement = '2018/09'
        elif '2018/08' in df.columns:
            year_settlement = '2018/08'
        elif '2018/12' in df.columns:
            year_settlement = '2018/12'

        if year_settlement is None:
            print(stock_item[1] + ",n/a")
            continue

        df = df[year_settlement]
        df1 = df.iloc[[0]]
        df2 = df.loc[['발행주식수']]

        if type(df1.values[0]) == np.float64 and math.isnan(df1.values[0]):
            continue
        if type(df1.values[0]) == np.float64 and math.isnan(df2.values[0]):
            continue

        sales = int(df1.values[0])
        issued_stock_count = int(df2.values[0])
        year_first_stock_price = naver.get_2019_first_stock_price(code, None)

        if year_first_stock_price is None:
            continue

        market_capitalization = issued_stock_count * int(year_first_stock_price.split("|")[4])

        price_gap = sise.get_increase_rate_by_code(code, None)

        if price_gap is None:
            continue

        psr = 0
        if sales == 0:
            psr = str(psr)
        else:
            psr = str(round(market_capitalization / sales, 2))

        print(stock_item[1] + "," + str(market_capitalization) + "," + str(sales) + "," + psr
              + "," + str(price_gap[0]) + "," + price_gap[1] + "," + str(price_gap[2]) + "," + str(price_gap[3]) + "," + year_settlement)


    #df = pd.DataFrame(columns=("종목명", "PSR"))
    #df = df.append({"종목명": "삼성전자", "PSR": 31111}, ignore_index=True)

    #df.to_csv("../result/result.csv")


chapter8_035()