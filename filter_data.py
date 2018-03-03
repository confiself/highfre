#! coding:utf-8
import re
import json


def get_trade_data():
    trac_dict = {}
    last_trac_time = None
    _count = 0
    with open('/tmp/ws.log.4') as f, \
            open('/tmp/ws.log.4.trade', 'w', encoding='utf-8') as f_w:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            info = re.sub('^.* INFO ', repl='', string=line)
            if 'data' in info and '"table": "trade"' in info and 'action' in info:
                info = eval(info)
                if info['action'] == 'insert':
                    for data in info['data']:
                        f_w.writelines(json.dumps(data) + '\n')
                        trac_dict[data['trdMatchID']] = data['timestamp']
                        last_trac_time = data['timestamp']
                        _count += 1
                elif info['action'] == 'partial':
                    # 由于网络中断引起
                    f_w.writelines('partial' + '\n')

                    print('partial')
                    for data in info['data']:
                        timestamp = data['timestamp'][:16]
                        if last_trac_time and timestamp < last_trac_time[:16]:
                            print('data exists time')
                            continue
                        if data['trdMatchID'] in trac_dict:
                            print('data exists id')
                            continue
                        f_w.writelines(json.dumps(data) + '\n')
                        trac_dict[data['trdMatchID']] = data['timestamp']
                        _count += 1
            if _count % 1000 == 0:
                print(_count)


if __name__ == '__main__':
    get_trade_data()