#! coding:utf-8
import requests

def get_data():
    # print(requests.get('https://www.okex.com/v2/markets/tickers', verify=False).content)
    print(requests.get('https://www.okex.com/v2/futures/pc/market/marketOverview.do?symbol=f_usd_all', verify=False).content)


if __name__ == '__main__':
    get_data()
