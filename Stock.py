
class Stock:

    # 아래 데이터 소스 http://www.krx.co.kr/main/main.jsp -> 시장정보 -> 상장현황 -> 상장종목 검색 -> csv 다운로드
    stock_item_list_file = 'data/market_stock_item_data.csv'

    def main(self):
        stock_item_list = self.get_all_stock_item_list()

        for stock in stock_item_list:
            print(stock[0] + ' ' + stock[1])

    def get_all_stock_item_list(self):

        file = open(self.stock_item_list_file, 'rt', encoding='utf8')

        stock_item_list = []

        for line in file.readlines():
            token = line.split(',')
            if len(token) > 3:
                item = (token[1], token[2])
                stock_item_list.append(item)

        return stock_item_list


if __name__ == '__main__':
    Stock().main()
