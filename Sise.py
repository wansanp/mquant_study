import requests
from bs4 import BeautifulSoup


class Sise:

    # 아래 데이터 소스 http://www.krx.co.kr/main/main.jsp -> 시장정보 -> 상장현황 -> 상장종목 검색 -> csv 다운로드
    stock_item_list_file = 'data/market_stock_item_data.csv'

    default_querying_size = '500'

    def main(self):

        name = "코오롱티슈진"

        result = self.get_increase_rate_by_name(name, None)

        print(str(result[0]) + " " + result[1])

    def get_increase_rate_by_name(self, name, size):

        if size is None:
            size = self.default_querying_size

        code = self.find_code_by_name(name)
        data = self.get_increase_rate_by_code(code, size)

        return data

    def get_increase_rate_by_code(self, code, size):

        if size is None:
            size = self.default_querying_size

        first = self.get_2018_first_price(code, size)
        latest = self.get_latest_price(code)

        if first is None:
            return None

        # cover the case likes '20190102|0|0|0|2780|0'
        if first.split('|')[1] == '0':
            first = first.split('|')[4]
        else:
            first = first.split('|')[1]

        latest = latest.split('|')[4]

        data = self.compare_prices(first, latest)

        return data

    def get_all_data_by_name(self, name, size):

        if size is None:
            size = self.default_querying_size

        code = self.find_code_by_name(name)
        self.get_all_data_by_code(code, size)

    def get_all_data_by_code(self, code, size):

        if size is None:
            size = self.default_querying_size

        req = requests.get('https://fchart.stock.naver.com/sise.nhn?symbol='+code+'&timeframe=day&count='+size+'&requestType=0')
        xml = req.text
        soup = BeautifulSoup(xml, 'html.parser')
        items = soup.find_all("item")

        print('날짜,시가,고가,저가,종가,거래량')

        for item in items:
            data = item.get('data').replace('|', ',')
            print(data)

    def get_all_stock_item(self):

        file = open(self.stock_item_list_file, 'rt', encoding='utf8')

        stock_item_dict = {}

        for line in file.readlines():
            token = line.split(',')
            if len(token) > 10:
                stock_item_dict[token[2]] = str(token[1])

        return stock_item_dict

    def find_code_by_name(self, name):

        stock_item_dict = self.get_all_stock_item();

        code = stock_item_dict[name]

        return code

    def get_latest_price(self, code):

        req = requests.get('https://fchart.stock.naver.com/sise.nhn?symbol='+code+'&timeframe=day&count=1&requestType=0')
        xml = req.text
        soup = BeautifulSoup(xml, 'html.parser')
        items = soup.find_all("item")

        data = items[0].get('data')

        return data

    def get_2018_first_price(self, code, size):

        if size is None:
            size = self.default_querying_size

        req = requests.get('https://fchart.stock.naver.com/sise.nhn?symbol='+code+'&timeframe=day&count='+size+'&requestType=0')
        xml = req.text
        soup = BeautifulSoup(xml, 'html.parser')
        items = soup.find_all("item")

        data = None

        for item in items:

            if item.get('data').split('|')[0] == '20190102':
                data = item.get('data')

        return data

    def compare_prices(self, first, current):

        first = int(first)
        current = int(current)

        result_price = current / first
        result_price = round(result_price, 3)
        result = "보합"

        if current > first:
            result = "상승"

        if first > current:
            result = "하락"

        data = (result_price, result, first, current)

        return data


if __name__ == '__main__':
    Sise().main()
