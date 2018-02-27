#!/bin/python
# encoding: utf-8

import time
import logging

from trader import Trader
import sys
import getopt

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='[%Y-%m_%d %H:%M:%S]',
                    filename='trade.log',
                    filemode='a')
_logger = logging.getLogger(__name__)


def main_loop(_trade_env):
    trader = Trader(_trade_env)

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
    trade_env = "test"
    opts, _ = getopt.getopt(sys.argv[1:], "e:")
    for opt, value in opts:
        if opt == '-e' and value in ['test', 'product']:
            trade_env = value
    _logger.info(trade_env)
    main_loop(trade_env)
