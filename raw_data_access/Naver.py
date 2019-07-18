import requests
from bs4 import BeautifulSoup


class Naver:

    default_querying_size = 500
    sise_url_prefix = 'https://fchart.stock.naver.com/sise.nhn?symbol='
    sise_url_suffix = '&requestType=0&timeframe=day'

    def get_all_data_by_code(self, code, size):

        if size is None:
            size = self.default_querying_size

        req = requests.get(self.sise_url_prefix + code + '&count=' + str(size) + self.sise_url_suffix)
        xml = req.text
        soup = BeautifulSoup(xml, 'html.parser')
        items = soup.find_all("item")

        data = []

        # 날짜,시가,고가,저가,종가,거래량
        for item in items:
            data.append(item.get('data'))

        return data

    def get_latest_stock_price(self, code):

        data = self.get_all_data_by_code(code, 1)

        return data[0]

    def get_2019_first_stock_price(self, code, size):

        items = self.get_all_data_by_code(code, size)

        data = None

        for item in items:

            if item.split("|")[0] == '20190102':
                data = item

        return data
