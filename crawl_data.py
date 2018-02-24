#! coding:utf-8
import requests
import time
import re
import json
import datetime
import os


def get_history(crawl_start_time, crawl_stop_time, reso):
    def _get():
        try:
            resp = requests.get(verify=False,

                                url='https://www.bitmex.com/api/udf/history?symbol=XBTUSD&resolution={}&from={}&to={}'.format(
                                    reso, crawl_start_time,
                                    crawl_stop_time))
            result_dict = json.loads(resp.text)
            if 'error' in resp.text:
                print(resp.text)
                return None
            if 'c' in result_dict and len(result_dict['c']) > 1:
                result_dict['resolution'] = reso
                return result_dict
        except:
            print('get error, retry after 3 seconds ...')
            return None
        return None
    max_retry_times = 1
    while max_retry_times > 0:
        result = _get()
        if result:
            return result
        time.sleep(5)
        max_retry_times -= 1
    return None


def get_data_by_day(start, end):
    date_start = datetime.datetime.strptime(start, '%Y-%m-%d')
    date_end = datetime.datetime.strptime(end, '%Y-%m-%d')
    while date_start <= date_end:
        crawl_date = date_start.strftime('%Y-%m-%d')
        date_start += datetime.timedelta(days=1)
        file_path = os.path.join('/Users/huzhenghui/opt/app/data/bitmex', str(crawl_date))
        if os.path.exists(file_path):
            continue
        _data_list = []
        resolution_list = ['1', '5', '60']
        for resolution in resolution_list:
            start_time = str(crawl_date) + ' 00:00:01'
            start_time = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
            start_time = re.sub('\..*', '', str(start_time))
            stop_time = str(crawl_date) + ' 23:59:59'
            stop_time = time.mktime(time.strptime(stop_time, '%Y-%m-%d %H:%M:%S'))
            stop_time = re.sub('\..*', '', str(stop_time))
            _data = get_history(start_time, stop_time, resolution)
            if not _data:
                break
            _data_list.append(_data)
        if len(_data_list) == len(resolution_list):  # 只有全部采采集完整才保存，否则跳过
            with open(file_path, 'w') as f:
                for _data in _data_list:
                    f.writelines(json.dumps(_data, ensure_ascii=False) + '\n')
if __name__ == '__main__':
    # get_history()
    get_data_by_day(start='2018-02-01', end='2018-02-15')
