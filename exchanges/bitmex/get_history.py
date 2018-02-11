#! coding:utf-8
import requests
import time
import re
import json

def get_history(start_time, stop_time,reso):
    """
    获取从2017年6月起的数据
    :return:
    """
    start_time = time.mktime(time.strptime('2018-02-11 00:00:00', '%Y-%m-%d %H:%M:%S'))
    start_time = re.sub('\..*', '', str(start_time))
    stop_time = re.sub('\..*', '', str(time.time()))
    print(str(start_time))
    print(stop_time)
    resp = requests.get(verify=False,
        url='https://www.bitmex.com/api/udf/history?symbol=XBTUSD&resolution={}&from={}&to={}'.format(reso, start_time,
                                                                                                    stop_time))
    # resp = dict(resp.text)
    # print(resp)
    # print(resp.keys())
    print(resp.text)
    result = json.loads(resp.text)
    print(result.keys())

def get_minute():



if __name__ == '__main__':
    get_history()
