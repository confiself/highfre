import matplotlib.pyplot as plt
import json
import datetime
import os
import numpy as np
import time
TIME_INTERVAL = 5


def plot_data():
    with open('/Users/huzhenghui/opt/app/data/bitmex/2017-09-27') as f:
        lines = f.readlines()
        label_list = ['1min', '5min', '1h']
        for i, line in enumerate(lines):
            line = line.strip()
            # plt.figure(label_list[i])
            data = json.loads(line.strip())
            plt.plot(data['t'], data['o'])
        plt.show()


def get_abnormal_minute(start, end):
    """
    寻找异常的点
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

        with open(file_path) as f:
            lines = f.readlines()
            data_1_minute = json.loads(lines[1].strip())
            # data_1_minute['t'] = [(x - data_1_minute['t'][0]) / 60 for x in data_1_minute['t']]
            # plt.bar(data_1_minute['t'][:100], data_1_minute['v'][:100], bottom=0.8, facecolor="#9999ff", edgecolor="white")
            abnormal_t_list = []
            skip_index = TIME_INTERVAL

            def _get_first_trigger(_base_index):
                value_h = data_1_minute['h'][_base_index]
                _base_key = 'more'
                if data_1_minute['o'][_base_index] > data_1_minute['c'][_base_index]:
                    _base_key = 'less'
                value_trigger_more = value_h * 1.01
                value_trigger_less = value_h * 0.99
                for _index in range(_base_index, len(data_1_minute['t'])):
                    if data_1_minute['h'][_index] >= value_trigger_more:
                        oc_dict[_base_key]['more'] += 1
                        return _base_key, 'more', data_1_minute['h'][_index]
                    if data_1_minute['l'][_index] <= value_trigger_less:
                        oc_dict[_base_key]['less'] += 1
                        return _base_key, 'less', data_1_minute['l'][_index]

            for i, v in enumerate(data_1_minute['v']):
                if i < skip_index:
                    continue
                if i > len(data_1_minute['t']) - TIME_INTERVAL:
                    break
                average = np.mean(data_1_minute['v'][i-TIME_INTERVAL:i])
                max_value = max(data_1_minute['v'][i-TIME_INTERVAL:i])
                current_v = data_1_minute['v'][i]
                if current_v > 2 * average and max_value < current_v * 0.9:
                    state = _get_first_trigger(i)
                    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data_1_minute['t'][i]))
                    print('find it', data_1_minute['t'][i], dt, state)
                    skip_index = i + TIME_INTERVAL
                    # abnormal_t_list.append(data_1_minute['t'][i])
            # plt.plot(abnormal_t_list, [100000] * len(abnormal_t_list), '*')
            # plt.show()
        print(oc_dict)


if __name__ == '__main__':
    # plot_data()
    get_abnormal_minute('2018-02-20', '2018-02-24')