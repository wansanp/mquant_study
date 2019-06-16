import pandas as pd
from Sise import Sise


class Stock:

    # 아래 데이터 소스 http://www.krx.co.kr/main/main.jsp -> 시장정보 -> 상장현황 -> 상장종목 검색 -> csv 다운로드
    stock_item_list_file = 'data/market_stock_item_data.csv'

    def main(self):
        #self.get_dividend_rate_2017_2018()
        #self.get_roe_ev_ebitda_2018()
        self.get_all_stock_category()

    def get_roe_ev_ebitda_2018(self):
        stock_item_list = self.get_all_stock_item_list()

        print('종목명,ROE(자본수익률),EV/EABITDA(이익수익률)')

        sise = Sise()

        for stock in stock_item_list:
            data = self.get_roe_ev_ebitda_per_code(stock[0])
            increase_rate = sise.get_increase_rate_by_code(stock[0], None)

            if data is None:
                print(stock[1] + "n/a, n/a, n/a, n/a, n/a, n/a")
            else:
                if increase_rate is None:
                    print(stock[1] + "," + data[0] + "," + data[1] + ", n/a, n/a, n/a, n/a")
                else:
                    print(stock[1] + "," + data[0] + "," + data[1] + "," + str(increase_rate[0]) + "," + increase_rate[1] + "," + str(increase_rate[2]) + "," + str(increase_rate[3]))

    def get_dividend_rate_2017_2018(self):
        stock_item_list = self.get_all_stock_item_list()

        print('종목명,2017,2018')

        for stock in stock_item_list:
            data = self.get_dividend_rate_per_code(stock[0])

            if data is None:
                print(stock[1] + ',0,0')
            else:
                print(stock[1] + ',' + data[0] + ',' + data[1])

    def get_all_stock_item_list(self):

        file = open(self.stock_item_list_file, 'rt', encoding='utf8')

        stock_item_list = []

        for line in file.readlines():
            token = line.split(',')
            item = (token[1], token[2], token[3])
            stock_item_list.append(item)

        stock_item_list = stock_item_list[1:]

        return stock_item_list

    def get_dividend_rate_per_code(self, code):

        url = 'https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?gicode=A' + code

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

    def get_roe_ev_ebitda_per_code(self, code):

        # 자본 수익률 : ROE (Return On Equity) = 순이익 / 자기자본 * 100 = 높을 수록 좋다
        # 이익 수익률 : EV/EBITDA = 기업 가치 (시가총액 + 순차입금) / 순이익 (이자비용, 감가상각비, 세금 빼기 전) = 낮을 수록 좋다

        url = 'https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?gicode=A'+code

        tables = pd.read_html(url)

        df = None

        for table in tables:
            if '구분' in table.columns:
                df = table
                break

        if df is None:
            return None

        df = df.set_index('구분')

        df = df[df.columns[0]]

        df = df.loc[['ROE', 'EV/EBITDA']]

        roe = str(df['ROE'])
        if roe == 'nan' or roe == '완전잠식' or roe == 'N/A(IFRS)':
            roe = 'n/a'
        if roe != 'n/a' and float(roe) < 0:
            roe = 'n/a'

        ev_ebitda = str(df['EV/EBITDA'])
        if ev_ebitda == 'nan':
            ev_ebitda = 'n/a'
        if ev_ebitda != 'n/a' and float(ev_ebitda) < 0:
            ev_ebitda = 'n/a'

        data = (roe, ev_ebitda)

        return data

    def get_all_stock_category(self):

        file = open(self.stock_item_list_file, 'rt', encoding='utf8')

        category_item_list = []

        for line in file.readlines():
            token = line.split(',')
            category_item_list.append(token[3] + "," + token[4])

        category_item_list = list(set(category_item_list))

        for category in category_item_list:
            print(category)


if __name__ == '__main__':
    Stock().main()
