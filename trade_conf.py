#! coding:utf-8


class TradeConf(object):

    def __init__(self, trade_env):
        if trade_env == 'test':
            self.api_key = "euYaAVNoDkTOnuJbIzdkbm2i"
            self.api_secret = "0EuDEoejFvYVPdFk5QlzCJGYM_u-nV1vB1aIstsLi697h_Nd"
        elif trade_env == 'product':
            self.api_key = "mW5LZginZQojCKQ9qLD8VfcS"
            self.api_secret = "OmYU1mcN92b2ClpQ2qJcoz5XT4-AjQKJ0sHBWRyaWt8gBJqD"

