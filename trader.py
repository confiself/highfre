#! coding:utf-8


class Trader:

    def __init__(self):
        self.current_order = None
        self.wallet = Wallet()
        self.qty_per_order = config.configuration['qty_per_order']

    def trade(self, suggest):
        self.suggest = suggest
        self.current_order = self._create_order()
        self._make_orders(),

    def _create_order(self):


    def _make_orders(self):
        # TODO 并行化处理
        self._make_sell_order()
        self._make_buy_order()
        self._check_order_state()

    def _check_order_state(self):
        session = models.Session()
        try:
            if self.current_order.is_bought and self.current_order.is_sold:
                self.current_order.state = 'done'
                _logger.info('[TRADER] The order is done!')
                session.commit()
        except Exception as e:
            _logger.error(e)
            session.rollback()

    def _make_buy_order(self):
        buy_ex = Trader._exchanges[self.current_suggestion.buy_account.name]
        session = models.Session()
        try:
            # buy_ex.buy(self.current_suggestion.stock_qty, self.current_suggestion.buy_price)
            self.current_order.bought_time = datetime.datetime.now()
            self.current_order.is_bought = True
            session.commit()
            _logger.info('Buy Order made: {0}'.format(self.current_order.bought_time))
        except Exception as e:
            _logger.error(e)
            session.rollback()

    def _make_sell_order(self):
        sell_ex = Trader._exchanges[self.current_suggestion.sell_account.name]
        session = models.Session()
        try:
            # sell_ex.sell(self.current_suggestion.stock_qty, self.current_suggestion.sell_price)
            self.current_order.sold_time = datetime.datetime.now()
            self.current_order.is_sold = True
            session.commit()
            _logger.info('Sell Order made: {0}'.format(self.current_order.sold_time))
        except Exception as e:
            _logger.error(e)
            session.rollback()

    def _wait_balance(self):
        _logger.info('Waitig for balance...')
        time.sleep(1)

    def _wait_sms(self):
        pass
