import ast
import requests
from datetime import date, timedelta

class Krx:

    isin_code = 'KR7005930003'
    start_date = '2019/04/20'
    end_date = '2019/06/20'

    def main(self):

        start = date(int(self.start_date.split("/")[0]), int(self.start_date.split("/")[1]), int(self.start_date.split("/")[2]))
        end = date(int(self.end_date.split("/")[0]), int(self.end_date.split("/")[1]), int(self.end_date.split("/")[2]))

        delta = end - start

        day_price_data = self.get_day_price()
        short_stock_selling_data = self.get_short_stock_selling()

        print("년/월/일|종가|시가|고가|저가|거래대금|공매도거래대금|공매도잔고금액")

        for day in range(delta.days+1):
            d = start + timedelta(days=day)
            key = str(d).replace("-", "")
            if key in day_price_data:
                print(str(d).replace("-", "/") + "|" + day_price_data[key][0] + "|" + day_price_data[key][1] + "|" + day_price_data[key][2] + "|" + day_price_data[key][3] + "|" + day_price_data[key][4]
                      + "|" + short_stock_selling_data[key][2] + "|" + short_stock_selling_data[key][3])

    def get_day_price(self):

        otp = requests.get('http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?bld=MKD/04/0402/04020100/mkd04020100t3_02&name=chart')

        parameters = {
            'isu_cd': self.isin_code,
            'fromdate': self.start_date.replace("/", ""),
            'todate': self.end_date.replace("/", ""),
            'pagePath': '/contents/MKD/04/0402/04020100/MKD04020100T3T2.jsp',
            'code': otp.content
        }

        res = requests.post('http://marketdata.krx.co.kr/contents/MKD/99/MKD99000001.jspx', parameters)

        data = ast.literal_eval(res.text)['block1']

        result = {}

        for item in data:
            # tdd_clsprc : 종가
            # acc_trdval : 거래대금
            # tdd_opnprc : 시가
            # tdd_hgprc : 고가
            # tdd_lwprc : 저가
            result[item['trd_dd'].replace("/", "")] = (item['tdd_clsprc'], item['tdd_opnprc'], item['tdd_hgprc'], item['tdd_lwprc'], item['acc_trdval'])

        return result

    def get_short_stock_selling(self):

        # reverse engineered from the source at here https://finance.naver.com/item/short_trade.nhn?code=005930
        otp = requests.get('https://short.krx.co.kr/contents/COM/GenerateOTP.jspx?bld=SRT/02/02010100/srt02010100X&name=form')

        parameters = {
            'isu_cd': self.isin_code,
            'strt_dd': self.start_date.replace("/", ""),
            'end_dd': self.end_date.replace("/", ""),
            'pagePath': '/contents/SRT/02/02010100/SRT02010100X.jsp',
            'code': otp.content
        }

        res = requests.post('https://short.krx.co.kr/contents/SRT/99/SRT99000001.jspx', parameters)

        data = ast.literal_eval(res.text)['block1']

        result = {}

        for item in data:
            # cvsrtsell_trdvol : 공매도 거래량
            # str_const_val1 : 공매도 잔고량
            # cvsrtsell_trdval : 공매도 거래대금
            # str_const_val2 : 공매도 잔고금액
            result[item['trd_dd'].replace("/", "")] = (item['cvsrtsell_trdvol'], item['str_const_val1'], item['cvsrtsell_trdval'], item['str_const_val2'])

        return result


if __name__ == "__main__":
    Krx().main()

