from raw_data_access.Fnguide import Fnguide
from raw_data_access.Krx import Krx


def chapter_10_42_for_2019_2nd_quarter():
    # pbr, gp/a
    # gp/a = 매출총 이익/자산총계
    # http://www.stockpedia.co.kr/report/view/2912
    # pbr은 낮게, gp/a 는 높게
    # 문제점 : 'IFRS 연결'제무가 아닌 종목 'CJ씨푸드', '매출총이익'이 없는 종목 '메리츠금융지주'

    fnguide = Fnguide()
    krx = Krx()

    print('종목명,PBR,GP/A')

    stock_item_list = krx.get_all_stock_item_list()
    stock_item_list = stock_item_list[1200:]

    for stock_item in stock_item_list:

        df = None
        df = fnguide.get_fnguide_dataframe(stock_item[0], 'IFRS(연결)')

        if df is None:
            continue

        df = df.set_index('IFRS(연결)')
        if 'Net Quarter' not in df.columns:
            continue
        df = df['Net Quarter']

        if "2019/06" not in df.columns:
            continue

        series = df['2019/06']

        pbr = series[('PBR',)]
        asset = float(series[('자산총계',)])

        df = fnguide.get_fnguide_financial_dataframe(stock_item[0], 'IFRS(연결)')
        df = df.set_index('IFRS(연결)')

        series = df['2019/06']

        if '매출총이익' not in series.index:
            continue

        sales_profit = series['매출총이익']
        gpa = round(sales_profit/asset, 2)

        print(stock_item[1] + ',' + str(pbr) + ',' + str(gpa))


chapter_10_42_for_2019_2nd_quarter()