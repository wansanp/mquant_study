
class Sise:

    default_querying_size = 500

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
