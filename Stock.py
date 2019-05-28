import pandas as pd

class Stock:

    # 아래 데이터 소스 http://www.krx.co.kr/main/main.jsp -> 시장정보 -> 상장현황 -> 상장종목 검색 -> csv 다운로드
    stock_item_list_file = 'data/market_stock_item_data.csv'

    def main(self):
        stock_item_list = self.get_all_stock_item_list()

        for stock in stock_item_list:
            df = self.get_dividend_rate(stock[0])

            if df is not None:
                print(df)

    def get_all_stock_item_list(self):

        file = open(self.stock_item_list_file, 'rt', encoding='utf8')

        stock_item_list = []

        for line in file.readlines():
            token = line.split(',')
            if len(token) > 3:
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

        df.set_index('IFRS(연결)')

        df.columns = df.columns.map('|'.join).str.strip('|')

        for column in df.columns:
            print(column)

        column_list = []

        if 'Annual|2017/12' in df.columns:
            column_list.append('Annual|2017/12')

        if 'Annual|2018/12' in df.columns:
            column_list.append('Annual|2018/12')

        if len(column_list) == 0:
            return None

        df = df[column_list]

        for idx in df.index:
            print(idx)

        return df

if __name__ == '__main__':
    Stock().main()
