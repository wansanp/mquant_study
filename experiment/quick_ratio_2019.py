from raw_data_access.Krx import Krx
from raw_data_access.Fnguide import Fnguide

business_category_file = open("../data/business_category_code.csv", "rt", encoding="utf8")

business_map = {}

for business_category in business_category_file.readlines():
    token = business_category.strip().split(",")
    business_map[token[0]] = token[1]

krx = Krx()
fnguide = Fnguide()

stock_item_list = krx.get_all_stock_item_list()

print("종목명,19 결산 당좌비율,업종")

for stock_item in stock_item_list:
    df = fnguide.get_fnguide_financial_ratio_dataframe(stock_item[0], "IFRS(연결)")

    try:
        if df is None:
            print(stock_item[1] + ",N/A,N/A")
        else:
            df = df.set_index("IFRS(연결)")
            series = df.loc['당좌비율계산에 참여한 계정 펼치기']
            last_quick_ratio = str(series[-1])
            print(stock_item[1] + "," + last_quick_ratio + "," + business_map[stock_item[2]])
    except KeyError:
        print(stock_item[1] + ",N/A,N/A")
    except AttributeError:
        print(stock_item[1] + ",N/A,N/A")
    except ValueError:
        print(stock_item[1] + ",N/A,N/A")

