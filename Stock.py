import pandas as pd


class Stock:

    # 아래 데이터 소스 http://www.krx.co.kr/main/main.jsp -> 시장정보 -> 상장현황 -> 상장종목 검색 -> csv 다운로드
    stock_item_list_file = 'data/market_stock_item_data.csv'

    def main(self):
        stock_item_list = self.get_all_stock_item_list()

        print('종목명,2017,2018')

        for stock in stock_item_list:
            data = self.get_dividend_rate(stock[0])

            if data is None:
                print(stock[1] + ",0,0")
            else:
                print(stock[1] + "," + data[0] + "," + data[1])

    def get_all_stock_item_list(self):

        file = open(self.stock_item_list_file, 'rt', encoding='utf8')

        stock_item_list = []

        for line in file.readlines():
            token = line.split(',')
            if len(token) > 10:
                item = (token[1], token[2])
                stock_item_list.append(item)

        stock_item_list = stock_item_list[1:]

        return stock_item_list

    def get_dividend_rate(self, code):

        url = 'https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?gicode=A'+code

        tables = pd.read_html(url)

        df = None

        for table in tables:
            if 'IFRS(연결)' in table.columns:
                df = table
                break

        if df is None:
            return None

        df.columns = df.columns.droplevel()

        df = df.set_index('IFRS(연결)')

        column_list = []

        if '2017/12' in df.columns:
            column_list.append('2017/12')

        if '2018/12' in df.columns:
            column_list.append('2018/12')

        if len(column_list) == 0:
            return None

        df = df[column_list]

        if len(df.columns) == 2 and '2017/12' not in df.columns:
            df.columns = ['2018/12', 'n/a']

        if len(df.columns) == 3:
            df.columns = ['2017/12', '2018/12', 'n/a']

        df = df.loc[['배당수익률']]

        dividend_rate_2017 = str('0')
        dividend_rate_2018 = str('0')

        if '2017/12' in df.columns:
            dividend_rate_2017 = str(df['2017/12'][0])
            if dividend_rate_2017 == 'nan':
                dividend_rate_2017 = '0'

        if '2018/12' in df.columns:
            dividend_rate_2018 = str(df['2018/12'][0])
            if dividend_rate_2018 == 'nan':
                dividend_rate_2018 = '0'

        data = (dividend_rate_2017, dividend_rate_2018)

        return data


if __name__ == '__main__':
    Stock().main()
