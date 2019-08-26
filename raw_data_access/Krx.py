import ast
import requests
import pandas as pd
from datetime import datetime
from io import BytesIO

class Krx:

    stock_item_list_file = '../../data/market_stock_item_data.csv'

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

    def get_stock_master_total_rank(self, mode=1, date_str=None):
        # KRX MarketData 30015 시가총액 상/하위
        # 종목코드, 종목명, 현재가, 대비, 등락률, 거래량, 거래대금, 시가, 고가, 저가,
        # 시가총액, 시가총액비중(%), 상장주식수, 외국인, 보유주식수, 외국인, 지분율(%)
        if date_str == None:
            date_str = datetime.today().strftime('%Y%m%d')
        if mode == 1:
            filetype = 'csv'
        elif mode == 2:
            filetype = 'xls'

        gen_otp_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
        gen_otp_data = {
            'name': 'fileDown',
            'filetype': filetype,
            'url': 'MKD/04/0404/04040200/mkd04040200_01',
            'market_gubun': 'ALL',
            'indx_ind_cd': '',
            'sect_tp_cd': 'ALL',
            'schdate': date_str,
            'pagePath': '/contents/MKD/04/0404/04040200/MKD04040200.jsp',
        }
        r = requests.post(gen_otp_url, gen_otp_data)
        code = r.content
        down_url = 'http://file.krx.co.kr/download.jspx'
        down_data = {'code': code}
        down_header = {'Referer': 'http://marketdata.krx.co.kr/mdi'}
        r = requests.post(down_url, headers=down_header, data=down_data)

        if mode == 1:
            df = pd.read_csv(BytesIO(r.content), header=0, index_col=0, thousands=',', converters={'종목코드': str})
            df.to_csv('../data/krx_total_rank.csv', encoding='euc-kr')
        elif mode == 2:
            df = pd.read_excel(BytesIO(r.content), header=0, index_col=0, thousands=',', converters={'종목코드': str})
            df.to_excel('../data/krx_total_rank.xls', encoding='euc-kr')
        return df

    def get_stock_master_corporation_list(self, mode=1):
        # KRX KIND 상장법인목록
        # 회사명, 종목코드, 업종, 주요제품, 상장일, 결산월, 대표자명, 홈페이지, 지역
        data = {
            'method': 'download',
            'pageIndex': '1',
            'currentPageSize': '5000',
            'orderMode': '3',
            'orderStat': 'D',
            'searchType': '13',
            'fiscalYearEnd': 'all',
            'location': 'all',
        }
        r = requests.post('http://kind.krx.co.kr/corpgeneral/corpList.do', data=data)
        df = pd.read_html(BytesIO(r.content), header=0, index_col=0, converters={'종목코드': str})[0]

        if mode == 1:
            df.to_csv('../data/krx_kind_corporation_list.csv', encoding='euc-kr')
        elif mode == 2:
            df.to_excel('../data/krx_kind_corporation_list.xls', encoding='euc-kr')
        return df

    def get_stock_master_corporation_search(self, mode=2):
        # KRX 30029 상장회사검색
        # 번호, 종목코드, 기업명, 업종코드, 업종, 상장주식수(주), 자본금(원), 액면가(원), 통화구분. 대표전화, 주소
        if mode == 1:
            filetype = 'csv'
        elif mode == 2:
            filetype = 'xls'

        gen_otp_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
        gen_otp_data = {
            'name': 'fileDown',
            'filetype': filetype,
            'url': 'MKD/04/0406/04060100/mkd04060100_01',
            'market_gubun': 'ALL',
            'isu_cdnm': '전체',
            'isu_cd': '',
            'isu_nm': '',
            'isu_srt_cd': '',
            'sort_type': 'A',
            'std_ind_cd': '',
            'par_pr': '',
            'cpta_scl': '',
            'sttl_trm': '',
            'lst_stk_vl': '1',
            'in_lst_stk_vl': '',
            'in_lst_stk_vl2': '',
            'cpt': '1',
            'in_cpt': '',
            'in_cpt2': '',
            'mktpartc_no': '',
            'pagePath': '/contents/MKD/04/0406/04060100/MKD04060100.jsp',
        }
        r = requests.post(gen_otp_url, gen_otp_data)
        code = r.content
        down_url = 'http://file.krx.co.kr/download.jspx'
        down_data = {'code': code}
        down_header = {'Referer': 'http://marketdata.krx.co.kr/mdi'}
        r = requests.post(down_url, headers=down_header, data=down_data)

        if mode == 1:
            df = pd.read_csv(BytesIO(r.content), header=0, index_col=0, thousands=',', sep='delimiter', engine='python',
                             encoding='utf-8')
            df.to_csv('../data/krx_corporation_list.csv', encoding='euc-kr')
        elif mode == 2:
            df = pd.read_excel(BytesIO(r.content), header=0, index_col=0, thousands=',', converters={'종목코드': str})
            df.to_excel('../data/krx_corporation_list.xls', encoding='euc-kr')
        return df