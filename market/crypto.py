import time

import ccxt
import pandas as pd

from const import KLINE_TIMEFRAME_12HOUR, KLINE_TIMEFRAME_1DAY
from notification.discord_bot import DiscordBot
from strategy.trendmaster import detect_trend


class Crypto:

    def __init__(self):
        """ 初始化
        """
        self.discord = DiscordBot()

    def start_check_crypto(self):
        binance = ccxt.binance({
            'enableRateLimit': True, })
        self.check(binance, KLINE_TIMEFRAME_12HOUR)
        okex3 = ccxt.okex3({
            'enableRateLimit': True, })
        self.check(okex3, KLINE_TIMEFRAME_12HOUR)
        self.check(okex3, KLINE_TIMEFRAME_1DAY)
        gate = ccxt.gateio({
            'enableRateLimit': True, })
        self.check(gate, KLINE_TIMEFRAME_12HOUR)
        self.check(gate, KLINE_TIMEFRAME_1DAY)
        huobi = ccxt.huobipro({
            'enableRateLimit': True, })

    def check(self, exchange, interval):

        exchange.load_markets()
        if exchange.has['fetchOHLCV']:
            for symbol in exchange.markets:
                if symbol.find('BTC') == -1:
                    continue
                print("Checking", exchange.describe().get('name'), interval, symbol)
                time.sleep(exchange.rateLimit / 1000 * 1.2)  # time.sleep wants seconds
                list = exchange.fetch_ohlcv(symbol, interval, limit=100)
                candles = pd.DataFrame(list, columns=['TimeStamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
                candles.drop('TimeStamp', axis=1, inplace=True)
                trigger, desc = detect_trend(candles)
                if trigger:
                    print(exchange.describe().get('name'), interval, symbol, desc)
                    self.discord.send_text(
                        "{0} {1} {2} {3}".format(exchange.describe().get('name'), interval, symbol, desc))
                else:
                    print(exchange.describe().get('name'), interval, symbol, "not trigger")
