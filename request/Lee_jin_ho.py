from raw_data_access import Krx
from datetime import date, timedelta


class Leejinho:

    isin_code = 'KR7005930003'
    start_date = '2019/04/20'
    end_date = '2019/06/20'

    def main(self):

        start = date(int(self.start_date.split("/")[0]), int(self.start_date.split("/")[1]), int(self.start_date.split("/")[2]))
        end = date(int(self.end_date.split("/")[0]), int(self.end_date.split("/")[1]), int(self.end_date.split("/")[2]))

        delta = end - start

        krx = Krx.Krx()

        day_price_data = krx.get_day_price(self.isin_code, self.start_date, self.end_date)
        short_stock_selling_data = krx.get_short_stock_selling(self.isin_code, self.start_date, self.end_date)
        kospi_index_data = krx.get_kospi_kosdaq_index('kospi', self.start_date, self.end_date)
        kosdaq_index_data = krx.get_kospi_kosdaq_index('kosdaq', self.start_date, self.end_date)

        print("년/월/일|종가|시가|고가|저가|거래대금|공매도거래대금|공매도잔고금액|기관거래대금순매수|외국인거래대금순매수|코스피종가|코스닥종가")

        for day in range(delta.days+1):
            d = start + timedelta(days=day)
            key = str(d).replace("-", "")

            if key in day_price_data:

                amounts = krx.get_org_alien_amounts(isin_code=self.isin_code, date=key)

                print(str(d).replace("-", "/") + "|" + day_price_data[key][0] + "|" + day_price_data[key][1] + "|" + day_price_data[key][2] + "|" + day_price_data[key][3] + "|" + day_price_data[key][4]
                      + "|" + short_stock_selling_data[key][2] + "|" + short_stock_selling_data[key][3]
                      + "|" + amounts['기관합계'] + "|" + amounts['외국인']
                      + "|" + kospi_index_data[key] + "|" + kosdaq_index_data[key])


if __name__ == '__main__':
    Leejinho().main()