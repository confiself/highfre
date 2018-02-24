#! coding:utf-8
import time
import crawl_data
import re
import numpy as np
import logging

_logger = logging.getLogger(__name__)
TIME_INTERVAL = 5
MAX_RATIO = 0.9


class Suggestion:
    def __init__(self, can_go, buy_price):
        self.buy_price = buy_price
        self.buy_direction = 'less'
        self.sell_less_price = buy_price * 1.01
        self.sell_less_price = buy_price * 0.99
        self.can_go = can_go


class Model(object):
    def __init__(self):
        self.last_test_time = None
        self.data = {}

    def get_chance(self):
        _logger.info('start get chance')
        average = np.mean(self.data['v'][-2-TIME_INTERVAL:-2])
        max_value = max(self.data['v'][-2-TIME_INTERVAL:-2])
        current_v = self.data['v'][-2]
        _logger.info('current_v,average,max_value' + str(current_v)+',' + str(average) + ',' + str(max_value))
        if current_v > 2 * average and max_value < current_v * MAX_RATIO:
            _logger.warning('get chance')
            return True
        return None

    def evaluate(self):
        _logger.info('start evaluate')

        current_time = time.time()
        stop_time = re.sub('\..*', '', str(current_time))
        start_time = current_time - 300 * 12
        start_time = re.sub('\..*', '', str(start_time))
        current_prefix = int(str(start_time)[-4:]) % 300
        _logger.info('current prefix,' + str(current_prefix))
        # if current_prefix > 60:  # 超过60s机会已逝
        #     return None

        self.data = crawl_data.get_history(start_time, stop_time, 5)

        if not self.data:
            _logger.info('not data')
            return None
        return self.get_chance()

if __name__ == '__main__':
    model = Model()
    model.evaluate()





