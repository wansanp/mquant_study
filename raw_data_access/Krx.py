import ast
import requests


class Krx:

    stock_item_list_file = '../data/market_stock_item_data.csv'

    def get_day_price(self, isin_code, start_date, end_date):

        # http://marketdata.krx.co.kr/mdi#document=040204
        # krx menu 30040 일자별 시세

        otp = requests.get('http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?bld=MKD/04/0402/04020100/mkd04020100t3_02&name=chart')

        parameters = {
            'isu_cd': isin_code,
            'fromdate': start_date.replace("/", ""),
            'todate': end_date.replace("/", ""),
            'pagePath': '/contents/MKD/04/0402/04020100/MKD04020100T3T2.jsp',
            'code': otp.content
        }

        res = requests.post('http://marketdata.krx.co.kr/contents/MKD/99/MKD99000001.jspx', parameters)

        data = ast.literal_eval(res.text)['block1']

        result = {}

        for item in data:
            # trd_dd : 날짜
            # tdd_clsprc : 종가
            # acc_trdval : 거래대금
            # tdd_opnprc : 시가
            # tdd_hgprc : 고가
            # tdd_lwprc : 저가
            result[item['trd_dd'].replace("/", "")] = (item['tdd_clsprc'], item['tdd_opnprc'], item['tdd_hgprc'], item['tdd_lwprc'], item['acc_trdval'])

        return result

    def get_short_stock_selling(self, isin_code, start_date, end_date):

        # reverse engineered from the source at here https://finance.naver.com/item/short_trade.nhn?code=005930
        otp = requests.get('https://short.krx.co.kr/contents/COM/GenerateOTP.jspx?bld=SRT/02/02010100/srt02010100X&name=form')

        parameters = {
            'isu_cd': isin_code,
            'strt_dd': start_date.replace("/", ""),
            'end_dd': end_date.replace("/", ""),
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

    def get_kospi_kosdaq_index(self, index_type, start_date, end_date):

        # krx menu 80001 개별지수 추이

        type = None
        ind_type = None

        if index_type == "kospi":
            type = "3"
            ind_type = "1001"
        elif index_type == "kosdaq":
            type = "4"
            ind_type = "2001"

        otp = requests.get('http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?bld=MKD/13/1301/13010102/mkd13010102&name=form')

        parameters = {
            'type': type,
            'ind_type': ind_type,
            'period_strt_dd': start_date.replace("/", ""),
            'period_end_dd': end_date.replace("/", ""),
            'pagePath': '/contents/MKD/13/1301/13010102/MKD13010102.jsp',
            'code': otp.content
        }

        res = requests.post('http://marketdata.krx.co.kr/contents/MKD/99/MKD99000001.jspx', parameters)

        data = ast.literal_eval(res.text)['block1']

        result = {}

        for item in data:
            #indx : 종가
            result[item['work_dt'].replace("/", "")] = item['indx']

        return result

    def get_org_alien_amounts(self, isin_code, date):

        # krx menu 80019 투자자별거래실적 (개별종목)

        otp = requests.get('http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?bld=MKD/13/1302/13020303/mkd13020303&name=form')

        parameters = {
            'isu_cd': isin_code,
            'period_selector':'day',
            'fromdate': date,
            'todate': date,
            'pagePath': '/contents/MKD/13/1302/13020303/MKD13020303.jsp',
            'code': otp.content
        }

        res = requests.post('http://marketdata.krx.co.kr/contents/MKD/99/MKD99000001.jspx', parameters)

        data = ast.literal_eval(res.text)['block1']

        result = {}

        for item in data:
            # netaskval : 거래대금(원) 순매수
            if item['invst_nm'] == '기관합계' or item['invst_nm'] == '외국인':
                result[item['invst_nm']] = item['netaskval']

        return result

    def get_all_stock_item_list(self):

        file = open(self.stock_item_list_file, 'rt', encoding='utf8')

        stock_item_list = []
        total_cnt = None
        pre_line = ""
        file.readline()

        for line in file.readlines():
            line = pre_line + line
            token = line.split(',')
            if total_cnt is None:
                total_cnt = token[-1]
            if token[-1] != total_cnt:
                line = pre_line + line
                pre_line = line
                continue
            item = (token[1], token[2], token[3]) #종목코드, 종목명, 업종코드
            stock_item_list.append(item)
            pre_line = ""

        return stock_item_list
