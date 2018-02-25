#! coding:utf-8

import bitmex
import json
from bitmex_websocket import BitMEXWebsocket
from time import sleep
import logging

_logger = logging.getLogger(__name__)


class Wallet(object):
    def __init__(self):
        pass


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
    https://testnet.bitmex.com/api/explorer/#!/User/User_getWallet
    """

    def __init__(self, symbol='XBTUSD', api_key=None, api_secret=None):
        if not api_key:
            self.client = bitmex.bitmex()
        else:
            self.client = bitmex.bitmex(test=False, api_key=api_key, api_secret=api_secret)
        self.symbol = symbol

    def quote_get(self):
        try:
            result = self.client.Quote.Quote_get(symbol=self.symbol, count=1, reverse=True).result()
            if result and len(result) > 0 and len(result[0]) > 0 \
                    and 'askPrice' in result[0][0]:
                return result[0][0]
        except:
            _logger.error('net error')
            pass
        return None

    def order_new(self):
        """
        ordType: Limit Market MarketWithLeftOverAsLimit Stop StopLimit MarketIfTouched LimitIfTouched
        side: Buy Sell
        return [{'price','orderID'}]
        """
        # 限价开仓
        # resopnse = self.client.Order.Order_new(symbol=self.symbol,
        #                                        orderQty=order_qty,
        #                                        price=price).result()
        # 以比特币计算 市价开仓,如果已经有反向合约，默认会减仓
        # resopnse = self.client.Order.Order_new(symbol=self.symbol,
        #                                        side='Sell',
        #                                        ordType='Market',
        #                                        simpleOrderQty=0.000001
        #                                        ).result()

        # 盈利后市价平仓,Close 全仓
        # resopnse = self.client.Order.Order_new(symbol=self.symbol,
        #                                        side='Buy',
        #                                        ordType='MarketIfTouched',
        #                                        execInst='Close',
        #                                        stopPx=8825).result()
        # 超过一定价格后止损
        resopnse = self.client.Order.Order_new(symbol=self.symbol,
                                               side='Buy',
                                               ordType='Market',
                                               execInst='Close',
                                               ).result()
        print(resopnse)

    def make_order(self, side, simple_order_qty):
        response = self.client.Order.Order_new(symbol=self.symbol,
                                               side=side,
                                               simpleOrderQty=simple_order_qty,
                                               ordType='Market').result()
        if response and len(response) > 0 and 'orderID' in response[0]:
            return response[0]
        return None

    def make_close_order(self, side, price):
        response = self.client.Order.Order_new(symbol=self.symbol,
                                               side=side,
                                               price=price,
                                               ordType='Limit',
                                               execInst='Close').result()
        if response and len(response) > 0 and 'orderID' in response[0]:
            return response[0]
        return None

    def get_orders(self):
        """
        'ordStatus': 'Filled' 'new'
        :return:
        """
        resopnse = self.client.Order.Order_getOrders(symbol=self.symbol, reverse=True, count=3, start=0).result()
        # 'simpleLeavesQty': 0.0489
        print(resopnse)

    def get_order_status(self):
        try:
            response = self.client.Order.Order_getOrders(symbol=self.symbol, count=5, filter='{"open": true}', reverse=True).result()
            if response and len(response) > 0:
                _logger.info(response[0][0])
                return response[0][0]['ordStatus']
        except:
            _logger.error('net error')
        return

    def get_execution_status(self):
        try:
            response = self.client.Execution.Execution_get(symbol=self.symbol, count=2, reverse=True).result()
            if response and len(response) > 0:
                print(response[0])
        except:
            _logger.error('net error')
        return None

    def get_wallet(self):

        # 'account': 269141,
        # 'transactType': 'UnrealisedPNL',
        # 'amount': -173200, 未实现盈亏
        # 'fee': 0,
        # 'transactStatus': 'Pending',
        # 'address': 'XBTUSD',
        # 'transactTime': None,
        # 'walletBalance': 744321, 钱包余额
        # 'marginBalance': 571121, 保证金余额
        # 'timestamp': None,
        # 'tx': None,
        try:
            response = self.client.User.User_getWalletHistory().result()
            if response and len(response) > 0 and len(response) > 0 and 'amount' in response[0][0]:
                result = response[0][0]
                if 'Pending' in str(response[0]):
                    if result['transactStatus'] != 'Pending':
                        _logger.error('Pending seq error')
                    result['transactStatus'] = 'Pending'
                return result
        except:
            _logger.error('net error')
        return None

    def order_amend(self, order_id, price):
        self.client.Order.Order_amend(orderID=order_id, price=price).result()

    def order_cancel(self, order_id):
        self.client.Order.Order_cancel(orderID=order_id).result()
        # self.client.Order.Order_cancel(orderID=order_id).result()

    def order_cancel_all(self):
        # 取消所有未成交订单
        try:
            response = self.client.Order.Order_cancelAll().result()
            if response and response[1].status_code == 200:
                return True
        except:
            _logger.error('net error')
        return False

    def instrument_get(self):
        # start=500
        # reverse = True
        self.client.Instrument.Instrument_get(filter=json.dumps({'rootSymbol': 'XBT'})).result()

    def make_market_order(self, side, simple_order_qty):
        try:
            response = self.client.Order.Order_new(symbol=self.symbol,
                                                   side=side,
                                                   simpleOrderQty=simple_order_qty,
                                                   ordType='Market').result()
            if response and len(response) > 0 and 'orderID' in response[0]:
                return response[0]
        except:
            _logger.error('net error')
        return None

    def make_stop_loss_order(self, side):
        try:
            response = self.client.Order.Order_new(symbol=self.symbol,
                                                   side=side,
                                                   ordType='Market',
                                                   execInst='Close',
                                                   ).result()
            if response and len(response) > 0:
                return response[0]
        except:
            _logger.error('net error')
        return None

    def make_stop_profit_order(self, side, price):
        try:
            response = self.client.Order.Order_new(symbol=self.symbol,
                                                   side=side,
                                                   ordType='MarketIfTouched',
                                                   execInst='Close',
                                                   stopPx=price).result()
            if response and len(response) > 0:
                return response
        except:
            _logger.error('net error')
        return False


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
    # bitmex_ws = BitMexWS(api_key="euYaAVNoDkTOnuJbIzdkbm2i",
    #                      api_secret="0EuDEoejFvYVPdFk5QlzCJGYM_u-nV1vB1aIstsLi697h_Nd")
    # bitmex_ws = BitMexWS()
    # bitmex_ws.run()
    bm = BitMexHttp(api_key="euYaAVNoDkTOnuJbIzdkbm2i", api_secret="0EuDEoejFvYVPdFk5QlzCJGYM_u-nV1vB1aIstsLi697h_Nd")
    # bm.get_orders()
    print(bm.get_wallet())
    # print(bm.get_order_status())
    # bm.get_execution_status()
    # bm.order_new()
    # bm.order_cancel_all()
    # bm.order_cancel_all()
    # bm.order_new(order_qty=-1, price=9801.0)
    # bm.order_amend(order_id="3a8d86ce-2402-693a-0aaa-9179b6df6c8d", price=9005.0)
    # bm.order_cancel(order_id="3a8d86ce-2402-693a-0aaa-9179b6df6c8d")
    # bm.order_cancel_all()
