import requests
from lxml import html
import pandas

class Fnguide:

    url_prefix = 'https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?gicode=A'
    url_finance = 'https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?ReportGB=D&gicode=A'

    def get_stock_item_per(self, code):

        url = self.url_prefix + code

        page = requests.get(url)
        tree = html.fromstring(page.content)

        elements = tree.xpath('//div[@class="corp_group2"]//dl//dd')

        stock_item_per = elements[1].text
        business_category_per = elements[5].text

        per_pair = (stock_item_per, business_category_per)

        return per_pair

    def get_fnguide_financial_dataframe(self, code):

        url = self.url_prefix + code

        tables = pandas.read_html(url)

        df = None

        for table in tables:
            if 'IFRS(연결)' in table.columns:
                df = table
                break

        return df

    def get_fnguide_dataframe(self, code, column_name):

        url = self.url_prefix + code

        tables = pandas.read_html(url)

        df = None

        for table in tables:
            if column_name in table.columns:
                df = table
                break

        return df

    def get_per(self, code):
        url = self.url_prefix + code
        page = requests.get(url)
        tree = html.fromstring(page.content)

        elements = tree.xpath("//div[@id=\"corp_group2\"]/dl/dd")
        per = elements[0].text
        return per

    def get_pbr(self, code):
        url = self.url_prefix + code
        page = requests.get(url)
        tree = html.fromstring(page.content)

        elements = tree.xpath("//div[@id=\"corp_group2\"]/dl/dd")
        pbr = elements[3].text
        return pbr

    def get_cash_flow_201812(self, code):
        url = self.url_finance + code
        settlement_month = self.get_settlement_month(code)

        column = None
        if settlement_month == 6:
            column = "2018/06"
        elif settlement_month == 12:
            column = "2018/12"
        elif settlement_month == 1:
            column = "2019/01"
        elif settlement_month == 2:
            column = "2019/02"
        elif settlement_month == 3:
            column = "2019/03"
        elif settlement_month == 4:
            column = "2019/04"

        if column is None:
            return None

        tables = pandas.read_html(url)

        df = tables[4]

        df = df.set_index('IFRS(연결)')
        df = df.loc['영업활동으로인한현금흐름']

        index_2018 = None
        for index in df.index:
            if column in index:
                index_2018 = index

        if index_2018 is None:
            return None

        cash_flow = df[index_2018]

        return cash_flow

    def get_settlement_month(self, code):
        url = self.url_finance + code
        page = requests.get(url)
        tree = html.fromstring(page.content)
        elements = tree.xpath("//span[@class=\"stxt stxt3\"]")
        settlement_month = elements[0].text
        settlement_month = int(settlement_month.replace("월 결산", ""))

        return settlement_month
