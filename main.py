# -*- coding: UTF-8 -*-
import config
from market.crypto import Crypto
from market.stock import Stock


def go():
    config.config.loads('config.json')
    Crypto().start_check()
    Stock().start_check_china_stock()


if __name__ == '__main__':
    go()
