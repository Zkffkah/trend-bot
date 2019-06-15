import datetime

import baostock as bs
import pandas as pd

from notification.discord_bot import DiscordBot
from strategy.trendmaster import detect_trend


class Stock:

    def __init__(self):
        """ 初始化
        """
        self.discord = DiscordBot()

    def start_check_china_stock(self):
        login_result = bs.login(user_id='anonymous', password='123456')
        print('login respond error_msg:' + login_result.error_msg)

        today = datetime.datetime.now()

        # 获取交易日信息
        trade_date_rs = bs.query_trade_dates(start_date="2019-01-01",
                                             end_date=datetime.datetime.strftime(today, '%Y-%m-%d'))
        print('query_trade_dates respond error_code:' + trade_date_rs.error_code)
        print('query_trade_dates respond  error_msg:' + trade_date_rs.error_msg)
        data_list = []
        while (trade_date_rs.error_code == '0') & trade_date_rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(trade_date_rs.get_row_data())
        trade_date_df = pd.DataFrame(data_list, columns=trade_date_rs.fields)
        last_trade_date = trade_date_df[trade_date_df['is_trading_day'] == '1'].iloc[-1]['calendar_date']

        stock_rs = bs.query_all_stock(last_trade_date)
        print('query_all_stock respond error_code:' + stock_rs.error_code)
        print('query_all_stock respond  error_msg:' + stock_rs.error_msg)
        stock_df = stock_rs.get_data()

        for stockcode in stock_df["code"]:
            # 获取沪深A股行情和估值指标(日频)数据并返回收盘价20日均线 ####
            # date 日期
            # code 股票代码
            # close 收盘价
            # preclose 前收盘价
            # volume 交易量
            # amount 交易额
            # adjustflag 复权类型
            # turn 换手率
            # tradestatus 交易状态
            # pctChg 涨跌幅
            # peTTM 动态市盈率
            # psTTM 市销率
            # pcfNcfTTM 市现率
            # pbMRQ 市净率
            k_rs = bs.query_history_k_data("%s" % stockcode,
                                           "date,open,high,low,close,volume",
                                           # start_date=startdate,
                                           # end_date=last_trade_date,
                                           frequency="d",
                                           # adjustflag="2"
                                           )

            if k_rs.error_code != '0':
                print('query_history_k_data respond error_code:' + k_rs.error_code)
                print('query_history_k_data respond error_msg:' + k_rs.error_msg)
            result_list = []
            while (k_rs.error_code == '0') & k_rs.next():
                # 获取一条记录，将记录合并在一起
                result_list.append(k_rs.get_row_data())
            candles = pd.DataFrame(result_list, columns=k_rs.fields)
            candles.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'},
                           inplace=True)
            trigger, desc = detect_trend(candles)
            if trigger:
                print(stockcode, desc)
                self.discord.send_text(
                    "{0} {1}".format(stockcode, desc))
            else:
                print(stockcode, "not trigger")

        print('扫描结束')
        bs.logout()
