#! coding:utf-8
import matplotlib.pyplot as pm
import json
def plot_data():
    with open('/opt/app/data/bitmex/2017-09-27') as f:
        lines = f.readlines()
        label_list = ['1min', '5min', '1h']
        for i, line in enumerate(lines):
            line = line.strip()
            # pm.figure(label_list[i])
            data = json.loads(line.strip())
            pm.plot(data['t'], data['o'])
        pm.show()
class Trade(object):
    """
    1
    """
if __name__ == '__main__':
    plot_data()