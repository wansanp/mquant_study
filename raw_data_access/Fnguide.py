import requests
from lxml import html
import pandas

class Fnguide:

    url_prefix = 'https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?gicode=A'

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