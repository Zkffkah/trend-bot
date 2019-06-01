import numpy as np
import talib as ta

from indicator.heikinashi import heikin_ashi

last_index = -1
last_but_one_index = -2
last_but_two_index = -3
last_but_three_index = -4


def detect_trend(candles):
    ha_candles = heikin_ashi(candles)

    if ha_candles.shape[0] < 26:
        return False, ""

    ema26_lose = ta.EMA(ha_candles['HA_Close'].values, timeperiod=26)
    ema9_high = ta.EMA(np.insert(ha_candles['HA_High'].values, 0, [None, None, None], axis=0), timeperiod=9)  # offset 3
    ema9_low = ta.EMA(np.insert(ha_candles['HA_Low'].values, 0, [None, None, None], axis=0), timeperiod=9)  # offset 3

    if ha_candles['HA_Close'].iloc[last_but_one_index] > ema26_lose[last_but_one_index] and ha_candles['HA_Close'].iloc[
        last_but_one_index] > ema9_high[last_but_one_index - 3] \
            and not (
            ha_candles['HA_Close'].iloc[last_but_two_index] > ema26_lose[last_but_two_index] and
            ha_candles['HA_Close'].iloc[last_but_two_index] > ema9_high[last_but_two_index - 3]):
        range = (ha_candles['HA_High'].iloc[last_but_one_index] - ha_candles['HA_Open'].iloc[last_but_one_index]) / \
                ha_candles['HA_Open'].iloc[last_but_one_index]
        return True, "Possible Start Of Trend, range {:.2%} ".format(range)

    if ha_candles['HA_High'].iloc[last_but_one_index] > ha_candles['HA_High'].iloc[last_but_two_index] \
            and ha_candles['HA_Close'].iloc[last_but_two_index] > ema26_lose[last_but_two_index] and \
            ha_candles['HA_Close'].iloc[last_but_two_index] > ema9_high[last_but_one_index - 3] \
            and not (
            ha_candles['HA_Close'].iloc[last_but_three_index] > ema26_lose[last_but_three_index] and
            ha_candles['HA_Close'].iloc[last_but_three_index] > ema9_high[last_but_three_index - 3]):
        range = (ha_candles['HA_High'].iloc[last_but_one_index] - ha_candles['HA_Open'].iloc[last_but_one_index]) / \
                ha_candles['HA_Open'].iloc[last_but_one_index]
        return True, "Possible Long Entry, range {:.2%} ".format(range)

    return False, ""
