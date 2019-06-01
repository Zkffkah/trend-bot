import pandas as pd


def heikin_ashi(data):
    df = pd.DataFrame(data=data, columns=['Open', 'High', 'Low', 'Close', 'Volume'], dtype=float)
    heikin = pd.DataFrame()
    heikin['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4

    idx = df.index.name
    df.reset_index(inplace=True)
    heikin.reset_index(inplace=True)

    for i in range(0, len(df)):
        if i == 0:
            heikin.at[i, 'HA_Open'] = (df.at[i, 'Open'] + df.at[i, 'Close']) / 2
        else:
            heikin.at[i, 'HA_Open'] = (heikin.at[i - 1, 'HA_Open'] + heikin.at[i - 1, 'HA_Close']) / 2
            heikin.at[i, 'HA_Diff'] = heikin.at[i, 'HA_Close'] - heikin.at[i, 'HA_Open']

    if idx is None:
        idx = 'index'

    df.set_index(idx, inplace=True)
    heikin.set_index(idx, inplace=True)

    heikin['HA_High'] = pd.concat([heikin['HA_Open'], heikin['HA_Close'], df['High']], axis=1).max(axis=1)
    heikin['HA_Low'] = pd.concat([heikin['HA_Open'], heikin['HA_Close'], df['Low']], axis=1).min(axis=1)

    return heikin
