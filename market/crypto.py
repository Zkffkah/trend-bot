import time

import ccxt
import pandas as pd

from const import KLINE_TIMEFRAME_12HOUR, KLINE_TIMEFRAME_1DAY
from data.cryptowatch import crypto_watch_client
from notification.discord_bot import DiscordBot
from notification.telegram_bot import TelegramBot
from strategy.trendmaster import detect_trend


class Crypto:

    def __init__(self):
        """ 初始化
        """
        self.discord = DiscordBot()
        self.telegram = TelegramBot()

    def start_check(self):
        # self.start_check_from_cw()
        self.start_check_from_ccxt()

    def start_check_from_cw(self):
        binance = crypto_watch_client.Binance()
        self.check_cw_exchange(binance, KLINE_TIMEFRAME_12HOUR)
        okex = crypto_watch_client.Okex
        self.check_cw_exchange(okex, KLINE_TIMEFRAME_12HOUR)
        gateio = crypto_watch_client.Gateio
        self.check_cw_exchange(gateio, KLINE_TIMEFRAME_12HOUR)
        huobi = crypto_watch_client.Huobi
        self.check_cw_exchange(huobi, KLINE_TIMEFRAME_12HOUR)

    def start_check_from_ccxt(self):
        binance = ccxt.binance({
            'enableRateLimit': True, })
        self.check_ccxt_exchange(binance, KLINE_TIMEFRAME_12HOUR)
        okex3 = ccxt.okex3({
            'enableRateLimit': True, })
        self.check_ccxt_exchange(okex3, KLINE_TIMEFRAME_12HOUR)
        self.check_ccxt_exchange(okex3, KLINE_TIMEFRAME_1DAY)
        gate = ccxt.gateio({
            'enableRateLimit': True, })
        self.check_ccxt_exchange(gate, KLINE_TIMEFRAME_12HOUR)
        self.check_ccxt_exchange(gate, KLINE_TIMEFRAME_1DAY)
        huobi = ccxt.huobipro({
            'enableRateLimit': True, })

    def check_ccxt_exchange(self, exchange, interval):

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
                    # self.telegram.send_text(
                    #     "{0} {1} {2} {3}".format(exchange.describe().get('name'), interval, symbol, desc))
                else:
                    print(exchange.describe().get('name'), interval, symbol, "not trigger")

    def check_cw_exchange(self, exchange, interval):
        markets = exchange.load_markets()
        for market in markets:
            symbol = market.symbol
            if symbol.find('btc') == -1:
                continue
            print("Checking", exchange.describe().get('name'), interval, symbol)
            list = exchange.fetch_ohlcv(symbol, interval)[interval]
            candles = pd.DataFrame(list, columns=['TimeStamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'Unknown'])
            candles.drop(['TimeStamp', 'Unknown'], axis=1, inplace=True)
            trigger, desc = detect_trend(candles)
            if trigger:
                print(exchange.describe().get('name'), interval, symbol, desc)
                self.discord.send_text(
                    "{0} {1} {2} {3}".format(exchange.describe().get('name'), interval, symbol, desc))
                # self.telegram.send_text(
                #     "{0} {1} {2} {3}".format(exchange.describe().get('name'), interval, symbol, desc))
            else:
                print(exchange.describe().get('name'), interval, symbol, "not trigger")
