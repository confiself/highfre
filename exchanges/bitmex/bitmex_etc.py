#! coding:utf-8

import bitmex
import json
from bitmex_websocket import BitMEXWebsocket
import logging
from time import sleep

class BitMexHttp(object):
    """
    # 错误情况 429
    # 'X-RateLimit-Limit': '150',
    # 'X-RateLimit-Remaining': '147',
    # 'X-RateLimit-Reset': '1516119556'
    # result[1].headers
    # Retry-After
    # The system is currently overloaded. Please try again later.
    # 503 error
    # 500 milliseconds. 500ms 后重试
    """

    def __init__(self, symbol='XBTUSD', api_key=None, api_secret=None):
        if not api_key:
            self.client = bitmex.bitmex()
        else:
            self.client = bitmex.bitmex(test=False, api_key=api_key, api_secret=api_secret)
        self.symbol = symbol

    def quote_get(self):
        result = self.client.Quote.Quote_get(symbol=self.symbol, count=1, reverse=True).result()
        # 0{timestamp,bidSize,bidPrice,askPrice,askSize}, 1(headers,reason,status_code)
        print(result[0][0]['bidPrice'])
        print(result[0][0]['bidSize'])
        print(result[0][0]['askPrice'])
        # startTime=datetime.datetime(2018, 1, 1)
        # endTime=datetime.datetime.utcnow()
        return result

    def order_new(self, order_qty, price):
        resopnse = self.client.Order.Order_new(symbol=self.symbol, orderQty=order_qty, price=price).result()
        order_id = resopnse[0]['orderID']
        print(resopnse)

    def order_amend(self, order_id, price):
        self.client.Order.Order_amend(orderID=order_id, price=price).result()

    def order_cancel(self, order_id):
        self.client.Order.Order_cancel(orderID=order_id).result()
        # self.client.Order.Order_cancel(orderID=order_id).result()

    def order_cancel_all(self):
        self.client.Order.Order_cancelAll().result()

    def instrument_get(self):
        # start=500
        # reverse = True
        self.client.Instrument.Instrument_get(filter=json.dumps({'rootSymbol': 'XBT'})).result()


class BitMexWS(object):
    """
    适合订阅数据
    """

    def __init__(self, api_key=None, api_secret=None, symbol="XBTUSD"):
        endpoint = "https://testnet.bitmex.com/api/v1"
        if api_key:
            endpoint = "https://www.bitmex.com/api/v1"
        self.ws = BitMEXWebsocket(endpoint=endpoint,
                                  symbol=symbol,
                                  api_key=api_key,
                                  api_secret=api_secret)

    def run(self):
        logger = self.setup_logger()
        # Instantiating the WS will make it connect. Be sure to add your api_key/api_secret.

        logger.info("Instrument data: %s" % self.ws.get_instrument())

        # Run forever
        while self.ws.ws.sock.connected:
            logger.info("Ticker: %s" % self.ws.get_ticker())
            if self.ws.api_key:
                logger.info("Funds: %s" % self.ws.funds())
            logger.info("Market Depth: %s" % self.ws.market_depth())
            logger.info("Recent Trades: %s\n\n" % self.ws.recent_trades())
            sleep(10)

    def setup_logger(self):
        # Prints logger info to terminal
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)  # Change this to DEBUG if you want a lot more info
        ch = logging.StreamHandler()
        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # add formatter to ch
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger


if __name__ == '__main__':
    bitmex_ws = BitMexWS(api_key="euYaAVNoDkTOnuJbIzdkbm2i", api_secret="0EuDEoejFvYVPdFk5QlzCJGYM_u-nV1vB1aIstsLi697h_Nd")
    bitmex_ws = BitMexWS()
    bitmex_ws.run()
    # bm = BitMexHttp(api_key="euYaAVNoDkTOnuJbIzdkbm2i", api_secret="0EuDEoejFvYVPdFk5QlzCJGYM_u-nV1vB1aIstsLi697h_Nd")
    # bm.order_new(order_qty=-1, price=9801.0)
    # bm.order_amend(order_id="3a8d86ce-2402-693a-0aaa-9179b6df6c8d", price=9005.0)
    # bm.order_cancel(order_id="3a8d86ce-2402-693a-0aaa-9179b6df6c8d")
    # bm.order_cancel_all()


