import requests
from lxml import html
from Stock import Stock


class Index:

    def main(self):
        per_all_business_category_list = self.get_per_all_business_category()

        print('업종코드/업종PER/업종설명')

        for per_business_category in per_all_business_category_list:
            print(per_business_category[0] + "/" + per_business_category[1] + "/" + per_business_category[2])

    def get_business_category_code(self):

        file_path = 'data/business_category_code.csv'

        file = open(file_path, 'rt', encoding='utf-8')

        business_category_code_list = []

        for line in file.readlines():

            code = None
            description = None

            if len(line.split(",")) == 2:
                code = line.split(",")[0]
                description = line.split(",")[1].replace('\n', '')
            else:
                code = line[0: line.find(",")]
                description = line[line.find(",")+1: len(line)].replace('\n', '')

            business_category_code = (code, description)

            business_category_code_list.append(business_category_code)

        return business_category_code_list

    def get_per_all_business_category(self):

        per_all_business_category_code_list = []

        stock = Stock()

        business_category_code_list = self.get_business_category_code()

        for business_category_code in business_category_code_list:
            business_code = business_category_code[0]
            description = business_category_code[1]

            stock_item_list = stock.get_all_stock_item_list()

            for stock_item in stock_item_list:

                if stock_item[2] == business_code:

                    per_pair = self.get_stock_item_per(stock_item[0])
                    business_category_per = (business_code, per_pair[1], description)
                    per_all_business_category_code_list.append(business_category_per)
                    break

        return per_all_business_category_code_list

    def get_stock_item_per(self, code):

        url = 'https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?gicode=A' + code

        page = requests.get(url)
        tree = html.fromstring(page.content)

        elements = tree.xpath('//div[@class="corp_group2"]//dl//dd')

        stock_item_per = elements[1].text
        business_category_per = elements[5].text

        per_pair = (stock_item_per, business_category_per)

        return per_pair


if __name__ == '__main__':
    Index().main()
