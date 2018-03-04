import websocket
import hashlib
import time
import _thread
import logging
api_key = ''
secret_key = ""
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='[%Y-%m_%d %H:%M:%S]',
                    filename='okex.ws.log',
                    filemode='a')

# business
def buildMySign(params, secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) + '&'
    return hashlib.md5((sign + 'secret_key=' + secretKey).encode("utf-8")).hexdigest().upper()


# spot trade
def spotTrade(channel, api_key, secretkey, symbol, tradeType, price='', amount=''):
    params = {
        'api_key': api_key,
        'symbol': symbol,
        'type': tradeType
    }
    if price:
        params['price'] = price
    if amount:
        params['amount'] = amount
    sign = buildMySign(params, secretkey)
    finalStr = "{'event':'addChannel','channel':'" + channel + "','parameters':{'api_key':'" + api_key + "',\
                'sign':'" + sign + "','symbol':'" + symbol + "','type':'" + tradeType + "'"
    if price:
        finalStr += ",'price':'" + price + "'"
    if amount:
        finalStr += ",'amount':'" + amount + "'"
    finalStr += "},'binary':'true'}"
    return finalStr


# spot cancel order
def spotCancelOrder(channel, api_key, secretkey, symbol, orderId):
    params = {
        'api_key': api_key,
        'symbol': symbol,
        'order_id': orderId
    }
    sign = buildMySign(params, secretkey)
    return "{'event':'addChannel','channel':'" + channel + "','parameters':{'api_key':'" + api_key + "','sign':'" + sign + "','symbol':'" + symbol + "','order_id':'" + orderId + "'},'binary':'true'}"


# subscribe trades for self
def realtrades(channel, api_key, secretkey):
    params = {'api_key': api_key}
    sign = buildMySign(params, secretkey)
    return "{'event':'addChannel','channel':'" + channel + "','parameters':{'api_key':'" + api_key + "','sign':'" + sign + "'},'binary':'true'}"


# trade for future
def futureTrade(api_key, secretkey, symbol, contractType, price='', amount='', tradeType='', matchPrice='',
                leverRate=''):
    params = {
        'api_key': api_key,
        'symbol': symbol,
        'contract_type': contractType,
        'amount': amount,
        'type': tradeType,
        'match_price': matchPrice,
        'lever_rate': leverRate
    }
    if price:
        params['price'] = price
    sign = buildMySign(params, secretkey)
    finalStr = "{'event':'addChannel','channel':'ok_futuresusd_trade','parameters':{'api_key':'" + api_key + "',\
               'sign':'" + sign + "','symbol':'" + symbol + "','contract_type':'" + contractType + "'"
    if price:
        finalStr += ",'price':'" + price + "'"
    finalStr += ",'amount':'" + amount + "','type':'" + tradeType + "','match_price':'" + matchPrice + "','lever_rate':'" + leverRate + "'},'binary':'true'}"
    return finalStr


# future trade cancel
def futureCancelOrder(api_key, secretkey, symbol, orderId, contractType):
    params = {
        'api_key': api_key,
        'symbol': symbol,
        'order_id': orderId,
        'contract_type': contractType
    }
    sign = buildMySign(params, secretkey)
    return "{'event':'addChannel','channel':'ok_futuresusd_cancel_order','parameters':{'api_key':'" + api_key + "',\
            'sign':'" + sign + "','symbol':'" + symbol + "','contract_type':'" + contractType + "','order_id':'" + orderId + "'},'binary':'true'}"


# subscribe future trades for self
def futureRealTrades(api_key, secretkey):
    params = {'api_key': api_key}
    sign = buildMySign(params, secretkey)
    return "{'event':'addChannel','channel':'ok_sub_futureusd_trades','parameters':{'api_key':'" + api_key + "','sign':'" + sign + "'},'binary':'true'}"


def on_open(self):
    # subscribe okcoin.com spot ticker
    print("now open")
    # self.send("{'event':'addChannel','channel':'ok_sub_spotusd_btc_ticker','binary':'true'}")
    self.send("{'event':'addChannel','channel':'ok_sub_spot_btc_usdt_kline_1min'}");
    # subscribe okcoin.com future this_week ticker
    # self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_ticker_this_week','binary':'true'}")

    # subscribe okcoin.com future depth
    # self.send("{'event':'addChannel','channel':'ok_sub_futureusd_ltc_depth_next_week_20','binary':'true'}")

    # subscrib real trades for self
    # realtradesMsg = realtrades('ok_sub_spotusd_trades',api_key,secret_key)
    # self.send(realtradesMsg)


    # spot trade via websocket
    # spotTradeMsg = spotTrade('ok_spotusd_trade',api_key,secret_key,'ltc_usd','buy_market','1','')
    # self.send(spotTradeMsg)


    # spot trade cancel
    # spotCancelOrderMsg = spotCancelOrder('ok_spotusd_cancel_order',api_key,secret_key,'btc_usd','125433027')
    # self.send(spotCancelOrderMsg)

    # future trade
    # futureTradeMsg = futureTrade(api_key,secret_key,'btc_usd','this_week','','2','1','1','20')
    # self.send(futureTradeMsg)

    # future trade cancel
    # futureCancelOrderMsg = futureCancelOrder(api_key,secret_key,'btc_usd','65464','this_week')
    # self.send(futureCancelOrderMsg)

    # subscrbe future trades for self
    # futureRealTradesMsg = futureRealTrades(api_key,secret_key)
    # self.send(futureRealTradesMsg)


class OKEXWebSocket(object):

    def __init__(self):
        pass
        self.ws = None
        self.wst = None
        # self.url = "wss://real.okex.com:10440/websocket/okexapi"
        self.url = "wss://real.okcoin.com:10440/websocket/okcoinapi"
        self.logger = logging.getLogger(__name__)

    def on_message(self, ws, message):
        self.logger.info(message)

    def on_open(self, ws):
        # subscribe okcoin.com spot ticker
        self.logger.info("now open")
        # self.send("{'event':'addChannel','channel':'ok_sub_spotusd_btc_ticker','binary':'true'}")
        self.ws.send("{'event':'addChannel','channel':'ok_sub_spot_btc_usdt_kline_1min'}");

    def on_error(self, ws, error):
        self.logger.error('Error:' + error)

    def on_close(self, ws):
        self.logger.info("### closed ###")
        self.logger.info("### restart ###")
        self.start()

    def start(self):
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()
        self.wst = _thread.start_new_thread(self.ws.run_forever, ())
        self.wst.daemon = True
        self.wst.start()


if __name__ == "__main__":
    okex_ws = OKEXWebSocket()
    okex_ws.start()
    while True:
        print('ping...')
        okex_ws.ws.send('{"event":"ping"}')
        time.sleep(10)
