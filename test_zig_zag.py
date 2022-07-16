"""
Test code to show functionality of the zig-zag indicator
"""

import mplfinance as mpf
import numpy as np
import pandas as pd
import MetaTrader5 as mt5
from zig_zag import zig_zag, highest, lowest

# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

symbol = "EURUSD"
eurgbp_rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 600)

# shut down connection to MetaTrader 5
mt5.shutdown()

df = pd.DataFrame(eurgbp_rates)

df["Date"] = pd.to_datetime(df["time"], unit="s")

df.set_index("Date", inplace=True)

df.columns = ["Time", "Open", "High", "Low", "Close", "Volume", "Spread",
       "Real Volume"]

low_idx = lowest(df["Close"].to_numpy(), 12, 20)

zig_zag = zig_zag(np.flipud(df["High"].to_numpy()),
                  np.flipud(df["Low"].to_numpy()), 
                  point=0.00001, depth=12, deviation=5, back_step=3)


mpf.plot(
    df,
    type="candle",
    style="charles",
    title=symbol,
    ylabel="",
    volume=True,
    ylabel_lower="Tick\nVolume",
    show_nontrading=False)
