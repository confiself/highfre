#! coding:utf-8
import time
import crawl_data
import re
import numpy as np
import logging
import datetime
import json
import os

_logger = logging.getLogger(__name__)
TIME_INTERVAL = 5
MAX_RATIO = 0.9


class Model(object):
    def __init__(self):
        self.last_test_time = None
        self.data = {}

    def get_chance(self, current_index):
        _logger.info('start get chance')
        average = np.mean(self.data['v'][current_index - TIME_INTERVAL:current_index])
        max_value = max(self.data['v'][current_index - TIME_INTERVAL:current_index])
        current_v = self.data['v'][current_index]
        _logger.info('current_v,average,max_value' + str(current_v) + ',' + str(average) + ',' + str(max_value))
        if current_v > 1.5 * average and max_value < current_v * MAX_RATIO:
            return self.has_condition(current_index)
        return None

    def evaluate(self):
        _logger.info('start evaluate')

        current_time = time.time()
        stop_time = re.sub('\..*', '', str(current_time))
        start_time = current_time - 300 * 12
        start_time = re.sub('\..*', '', str(start_time))
        # current_prefix = int(str(start_time)[-4:]) % 300
        # _logger.info('current prefix,' + str(current_prefix))
        # if current_prefix > 60:  # 超过60s机会已逝
        #     return None

        self.data = crawl_data.get_history(start_time, stop_time, 5)

        if not self.data:
            _logger.info('not data')
            return None
        return self.get_chance(-1)  # -1 表示当前，－2为前完整5分钟

    def has_condition(self, current_index):
        """
        1 根据成交量，前一小时的交易曲线，k线过滤，减少误判带来的损失（市价提交相当于30%损失）
        2 评测1.02成交的比率
        :return:
        """
        price_diff = self.data['o'][current_index] - self.data['c'][current_index]
        if abs(price_diff) > 10:
            side = 'Sell' if price_diff > 0 else 'Buy'  # 推荐交易方式，跟涨或跟跌
            price = int((self.data['o'][current_index] + self.data['c'][current_index]) / 2)
            _logger.info('get chance ' + side + ',' + str(price))
            return {'side': side, 'price': price}
        return None

    def test(self, start, end):
        """
        数据回测
        model.test('2018-02-20', '2018-02-26')
        {'more': {'more': 4, 'less': 21}, 'less': {'more': 38, 'less': 8}}
        :return:
        """

        date_start = datetime.datetime.strptime(start, '%Y-%m-%d')
        date_end = datetime.datetime.strptime(end, '%Y-%m-%d')
        _root_path = '/Users/huzhenghui/opt/app/data/bitmex'
        oc_dict = {'more': {'more': 0, 'less': 0}, 'less': {'more': 0, 'less': 0}}

        while date_start <= date_end:
            _date = date_start.strftime('%Y-%m-%d')
            date_start += datetime.timedelta(days=1)
            file_path = os.path.join(_root_path, _date)

            def _get_first_trigger(_base_index, _side):
                _base_key = 'more'
                if self.data['o'][_base_index] > self.data['c'][_base_index]:
                    _base_key = 'less'
                    value_h_l = self.data['l'][_base_index]
                start_value = int((self.data['o'][_base_index] + self.data['c'][_base_index]) / 2)
                # start_value = self.data['o'][_base_index]
                trigger = False
                for _index in range(_base_index + 1, len(self.data['t'])):
                    if self.data['l'][_index] <= start_value * 0.99:
                        oc_dict[_base_key]['less'] += 1
                        trigger = True
                    if self.data['h'][_index] >= start_value * 1.01:
                        oc_dict[_base_key]['more'] += 1
                        trigger = True
                    if trigger:
                        return
                return

            with open(file_path) as f:
                lines = f.readlines()
                self.data = json.loads(lines[1].strip())
                skip_index = TIME_INTERVAL
                for i, v in enumerate(self.data['v']):
                    if i < skip_index:
                        continue
                    if i > len(self.data['t']) - TIME_INTERVAL:
                        break
                    side = self.get_chance(i)
                    if side:
                        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.data['t'][i]))
                        _get_first_trigger(i, side)

            print(oc_dict)


if __name__ == '__main__':
    model = Model()
    # model.evaluate()
    model.test('2018-03-01', '2018-03-01')
