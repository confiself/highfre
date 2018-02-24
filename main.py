#!/bin/python
# encoding: utf-8

import time
import logging

from trader import Trader
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='[%Y-%m_%d %H:%M:%S]',
                    filename='trade.log',
                    filemode='a')
_logger = logging.getLogger(__name__)


def main_loop(_side):
    trader = Trader(_side)

    try:
        while True:
            _logger.info('trading...')
            trader.trade()
            _logger.info('retry after 10 s ...')
            time.sleep(10)
    except Exception as e:
        print(e)
        _logger.error(e)
    finally:
        pass


if __name__ == '__main__':
    side = 'Sell'
    if len(sys.argv) > 1 and sys.argv[1] == 'Buy':
        side = 'Buy'
    main_loop(side)
