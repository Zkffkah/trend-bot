from urllib.parse import urlencode, urljoin, parse_qsl, urlunparse, urlparse

import requests

from const import KLINE_TIMEFRAME_1MINUTE, KLINE_TIMEFRAME_30MINUTE, KLINE_TIMEFRAME_15MINUTE, KLINE_TIMEFRAME_5MINUTE, \
    KLINE_TIMEFRAME_3MINUTE, KLINE_TIMEFRAME_1HOUR, KLINE_TIMEFRAME_2HOUR, KLINE_TIMEFRAME_4HOUR, KLINE_TIMEFRAME_6HOUR, \
    KLINE_TIMEFRAME_8HOUR, KLINE_TIMEFRAME_12HOUR, KLINE_TIMEFRAME_1DAY, KLINE_TIMEFRAME_3DAY

API_URL = 'https://api.cryptowat.ch/'


class ApiRequestException(Exception):
    def __init__(self, response):
        msg = "(%s) %s [%s]" % (response.status_code, response.reason, response.url)
        super(ApiRequestException, self).__init__(msg)

        self.response = response
        self.status_code = response.status_code
        self.reason = response.reason

class Market():
    def __init__(self, json):
        self.exchange = json['exchange']
        self.symbol = json['pair']
        self.session = requests.Session()


    def __str__(self):
        return "<Market> %s: %s" % (self.exchange, self.symbol)

    def __repr__(self):
        return self.__str__()


intervalDict = dict(
    {KLINE_TIMEFRAME_1MINUTE: 60,
     KLINE_TIMEFRAME_3MINUTE: 60 * 3,
     KLINE_TIMEFRAME_5MINUTE: 60 * 5,
     KLINE_TIMEFRAME_15MINUTE: 60 * 15,
     KLINE_TIMEFRAME_30MINUTE: 60 * 30,
     KLINE_TIMEFRAME_1HOUR: 60 * 60,
     KLINE_TIMEFRAME_2HOUR: 60 * 60 * 2,
     KLINE_TIMEFRAME_4HOUR: 60 * 60 * 4,
     KLINE_TIMEFRAME_6HOUR: 60 * 60 * 6,
     KLINE_TIMEFRAME_8HOUR: 60 * 60 * 8,
     KLINE_TIMEFRAME_12HOUR: 60 * 60 * 12,
     KLINE_TIMEFRAME_1DAY: 60 * 60 * 24,
     KLINE_TIMEFRAME_3DAY: 60 * 60 * 24 * 3,
     })

def _add_query_string(url, params):
    x = list(urlparse(url))
    q = dict(parse_qsl(x[4]))
    q.update(params)
    x[4] = urlencode(q)
    return urlunparse(x)

class CwExchange:

    def __init__(self, exchange, api_url=API_URL):
        self.api_url = api_url
        self.exchange = exchange
        self.session = requests.Session()

    def _raiseIfError(self, response):
        if (response.ok):
            return
        raise ApiRequestException(response)

    def _get_response(self, url):
        resp = self.session.get(url)
        self._raiseIfError(resp)
        return resp.json()


    def load_markets(self):
        url = urljoin(self.api_url, "markets/")
        url = urljoin(url, self.exchange)

        resp = self._get_response(url)
        res = [Market(x) for x in resp['result']]
        return res

    def fetch_ohlcv(self, symbol, interval=None, before=None, after=None):
        url = urljoin(urljoin(self.api_url, "markets/%s/%s/" % (self.exchange, symbol)), "ohlc")
        params = {}
        if before is not None:
            params['before'] = before
        if after is not None:
            params['after'] = after
        if (interval is not None) and (intervalDict[interval] is not None):
            params['periods'] = intervalDict[interval]
        url = _add_query_string(url, params)

        resp = self._get_response(url)
        res = {}
        for period in resp['result']:
            res[interval] = resp['result'][period]
        return res


class Binance(CwExchange):
    def __init__(self):
        super(Binance, self).__init__("binance")

    def describe(self):
        return {
            'name': 'binance',
        }


class Okex(CwExchange):
    def __init__(self):
        super(Okex, self).__init__("okex")

    def describe(self):
        return {
            'name': 'Okex',
        }


class Gateio(CwExchange):
    def __init__(self):
        super(Gateio, self).__init__("gateio")

    def describe(self):
        return {
            'name': 'Gateio',
        }


class Huobi(CwExchange):
    def __init__(self):
        super(Huobi, self).__init__("huobi")

    def describe(self):
        return {
            'name': 'Huobi',
        }
