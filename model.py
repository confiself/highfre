#! coding:utf-8
import time
import crawl_data
import re
import numpy as np



class Suggestion:
    def __init__(self, can_go, buy_price):
        self.buy_price = buy_price
        self.buy_direction = 'less'
        self.sell_less_price = buy_price * 1.01
        self.sell_less_price = buy_price * 0.99
        self.can_go = can_go


class Advisor(object):
    def __init__(self):
        self.last_test_time = None
        self.data = {}

    def get_chance(self):
        average = np.mean(self.data['v'][:-1])
        max_value = max(self.data['v'][:-1])
        current_v = self.data['v'][-1]
        if current_v > 2 * average and max_value < current_v * 2 / 3:
            base_price = self.data['h'][:-1]
            return Suggestion(True, base_price)
        return None

    def evaluate(self):
        current_time = time.time()
        print(current_time)
        stop_time = re.sub('\..*', '', str(current_time))
        if current_time - self.last_test_time < 300:
            return None
        start_time = current_time - 300 * 11
        self.data = crawl_data.get_history(start_time, stop_time, 5)
        if not self.data:
            return None
        return self.get_chance()






