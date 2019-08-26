import numpy as np
import math
from raw_data_access.Fnguide import Fnguide
from raw_data_access.Krx import Krx
from raw_data_access.Naver import Naver
from raw_data_process.Sise import Sise


def chapter8_036():

    krx = Krx()
    fnguide = Fnguide()
    sise = Sise()

    stock_item_list = krx.get_all_stock_item_list()

    # 종목명, per
    for stock_item in stock_item_list:

        per = fnguide.get_per(stock_item[0])
        if per is None:
            return None

        pbr = fnguide.get_pbr(stock_item[0])
        if pbr is None:
            return None

        #psr = 시가총액 / 매출액
        #pcr = 시가총액 / 영업현금흐름
        psr_pcr = get_psr_pcr(stock_item[0])
        if psr_pcr is None:
            return None

        sise_result = sise.get_increase_rate_by_code(stock_item[0], None)
        print(stock_item[1] + "," + per + "," + pbr + "," + psr_pcr[0] + "," + psr_pcr[1] + "," + str(sise_result[0]) + "," + str(sise_result[1]) + "," + str(sise_result[2]))


def get_psr_pcr(code):

    naver = Naver()
    fnguide = Fnguide()

    df = fnguide.get_fnguide_financial_dataframe(code)
    if df is None:
        return None

    if 'IFRS(연결)' not in df.columns or 'Annual' not in df.columns:
        return None

    df = df[['IFRS(연결)', 'Annual']]

    df.columns = df.columns.droplevel()
    df = df.set_index('IFRS(연결)')

    settlement_month = fnguide.get_settlement_month(code)

    column = None
    if settlement_month == 6:
        column = "2018/06"
    elif settlement_month == 12:
        column = "2018/12"
    elif settlement_month == 1:
        column = "2019/01"
    elif settlement_month == 2:
        column = "2019/02"
    elif settlement_month == 3:
        column = "2019/03"
    elif settlement_month == 4:
        column = "2019/04"

    if column is None:
        return None

    df = df[column]
    df1 = df.iloc[[0]]
    df2 = df.loc[['발행주식수']]

    if type(df1.values[0]) == np.float64 and math.isnan(df1.values[0]):
        return None
    if type(df1.values[0]) == np.float64 and math.isnan(df2.values[0]):
        return None

    sales = int(df1.values[0])
    issued_stock_count = int(df2.values[0])
    year_first_stock_price = naver.get_2019_first_stock_price(code, None)

    if year_first_stock_price is None:
        return None

    market_capitalization = issued_stock_count * int(year_first_stock_price.split("|")[4])

    psr = 0
    if sales == 0:
        psr = str(psr)
    else:
        psr = str(round(market_capitalization / sales, 2))

    cash_flow = fnguide.get_cash_flow_201812(code)
    if cash_flow is None:
        return None

    pcr = str(round(market_capitalization/cash_flow, 2))

    return (psr, pcr)


chapter8_036()