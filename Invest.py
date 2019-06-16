from Stock import Stock
from Index import Index
from Sise import Sise

class Invest:

    average_per_file_path = "data/business_category_average_per.csv"

    def main(self):

        index = Index()
        stock = Stock()
        sise = Sise()

        average_per_business_category_dict = self.read_average_per_file()
        stock_item_list = stock.get_all_stock_item_list()

        print("종목명/PER/업종PER/상승하락/2019시초가/현재가/업종코드/업종설명")

        for stock_item in stock_item_list:
            stock_code = stock_item[0]
            per_pair = index.get_stock_item_per(stock_code)
            stock_item_per = per_pair[0]
            business_average_per = per_pair[1]

            if stock_item_per == '-' or business_average_per == '-':
                continue
            if stock_item_per > business_average_per:
                continue

            increase_rate = sise.get_increase_rate_by_code(stock_code, None)

            if increase_rate is None:
                continue

            print(stock_item[1] + "/" + stock_item_per + "/" + business_average_per + "/" + str(increase_rate[0]) + "/"
                  + increase_rate[1] + "/" + str(increase_rate[2]) + "/" + str(increase_rate[3]) + "/"
                  + stock_item[2] + "/" + average_per_business_category_dict[stock_item[2]][1])

    def read_average_per_file(self):

        average_per_business_category_dict = {}

        with open(self.average_per_file_path, 'rt', encoding='utf-8)') as f:
            for line in f.readlines():
                data = line.split("/")
                business_code = data[0]
                business_average_per = data[1]
                description = data[2].replace('\n', '')

                average_per_business_category_dict[business_code] = (business_average_per, description)

        return average_per_business_category_dict


if __name__ == '__main__':
    Invest().main()
