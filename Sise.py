import requests
from bs4 import BeautifulSoup

class Sise:

    # 아래 데이터 소스 http://www.krx.co.kr/main/main.jsp -> 시장정보 -> 상장현황 -> 상장종목 검색 -> csv 다운로드
    stock_item_list_file = 'data/market_stock_item_data.csv'

    default_querying_size = '500'

    def main(self):

        name = "삼성전자"

        print('날짜,시가,고가,저가,종가,거래량')
        self.get_all_data_by_name(name, None)

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


if __name__ == '__main__':
    Sise().main()
