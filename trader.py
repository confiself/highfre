#! coding:utf-8
import bitmex_etc
from model import Model
import logging
from trade_conf import TradeConf
_logger = logging.getLogger(__name__)


class Trader:
    """
    1 盈利时让利润飞起来，这种机制不过难以实现
    """
    def __init__(self, trade_env):
        self.current_order = None
        trade_conf = TradeConf(trade_env)
        self.etc_http = bitmex_etc.BitMexHttp(api_key=trade_conf.api_key,
                                              api_secret=trade_conf.api_secret)
        self.model = Model()
        self.suggest = None
        self.is_pending = False
        self.wallet_info = None

    @staticmethod
    def get_opposite_side(side):
        side_dict = {'Sell': 'Buy', 'Buy': 'Sell'}
        return side_dict[side]

    @staticmethod
    def get_stop_loss_price(side, price):
        price_dict = {'Buy': 0.98, 'Sell': 1.02}
        return int(price_dict[side] * price)

    @staticmethod
    def get_stop_profit_price(side, price):
        price_dict = {'Buy': 1.01, 'Sell': 0.99}
        return int(price_dict[side] * price)

    def trade(self):
        _logger.info("enter trade process ...")
        self.wallet_info = self.etc_http.get_wallet()
        if not self.wallet_info:
            return
        _logger.info(self.wallet_info)

        if self.wallet_info['transactStatus'] == 'Pending':
            self.is_pending = True
        else:
            self.is_pending = False
            if self.current_order:
                open_order_status = self.etc_http.get_order_status()
                if open_order_status and open_order_status != 'New':
                    _logger.info('set current order none')
                    self._set_current_order(None)
            _logger.info("is not pending")

        # 在已经有订单状态下判断是否需要止损
        if self._force_close_order():
            return
        self._create_order()
        self._set_stop_profit_order()

    def _set_current_order(self, current_order):
        self.current_order = current_order

    def _set_stop_profit_order(self):
        if self.current_order and 'stop_profit_order' not in self.current_order:
            order = self.current_order
            sell_side = Trader.get_opposite_side(order['side'])
            sell_price = Trader.get_stop_profit_price(order['side'], order['price'])
            stop_profit_order = self.etc_http.make_stop_profit_order(side=sell_side, price=sell_price)
            if stop_profit_order:
                self.current_order['stop_profit_order'] = True
                _logger.info("make stop profit order success.")
            else:
                _logger.info("make stop profit order fail.")

    def _force_close_order(self):
        """
        止损
        :return:
        """

        if not self.is_pending or not self.current_order:
            return False
        real_time_info = self.etc_http.quote_get()
        _logger.info('quote info:' + str(real_time_info))
        sell_side = Trader.get_opposite_side(self.current_order['side'])
        sell_price = Trader.get_stop_loss_price(side=self.current_order['side'],
                                                price=self.current_order['price'])
        _logger.info(sell_side + ',' + str(sell_price))

        if (sell_side == 'Buy' and real_time_info['bidPrice'] > sell_price) or \
                (sell_side == 'Sell' and real_time_info['bidPrice'] < sell_price):
            _logger.info("force stop loss ...")
            self.etc_http.make_stop_loss_order(side=sell_side)
            # self.etc_http.order_cancel_all()
            return True
        return False

    def _create_order(self):
        """
        1 目前空仓才下单,10倍杠杆，占比全仓80%，比特币下单
        2 取消所有未成交订单
        3 市价开仓 返回price, order id
        3 设置止盈委托
        :return:
        """
        _logger.info('enter create order process')
        if self.is_pending or self.current_order:
            return None
        _side = self.model.evaluate()
        if not _side:
            _logger.info('no chance')
            return
        _logger.info('model evaluate true')

        if not self.etc_http.order_cancel_all():
            return None
        _logger.info("found chance and start make order...")
        order = self.etc_http.make_market_order(side=_side,
                                                simple_order_qty=self.wallet_info['walletBalance'] * 9 * 1e-8)
        if order:
            _logger.info("create order success")
            _logger.info(order)
            self._set_current_order(order)
        return True


if __name__ == '__main__':
    trader = Trader('test')
    trader.trade()
