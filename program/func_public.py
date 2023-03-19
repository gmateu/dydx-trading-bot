from constants import RESOLUTION
import time
from func_utils import *
import pandas as pd
import numpy as np
from pprint import pprint


#GET RELEVANT PERIODES
ISO_TIMES = get_ISO_times()
print(ISO_TIMES)

# Get Candles Historical
def get_candles_historical(client, market):

  # Define output
  close_prices = []

  # Extract historical price data for each timeframe
  for timeframe in ISO_TIMES.keys():

    # Confirm times needed
    tf_obj = ISO_TIMES[timeframe]
    from_iso = tf_obj["from_iso"]
    to_iso = tf_obj["to_iso"]

    # Protect rate limits
    time.sleep(0.2)

    # Get data
    candles = client.public.get_candles(
      market=market,
      resolution=RESOLUTION,
      from_iso=from_iso,
      to_iso=to_iso,
      limit=100
    )

    # Structure data
    for candle in candles.data["candles"]:
      close_prices.append({"datetime": candle["startedAt"], market: candle["close"] })

  # Construct and return DataFrame
  close_prices.reverse()
  return close_prices

#construct market prices
def construct_market_prices(client):
    #declare variables
    tradeable_markets=[]
    markets = client.public.get_markets()

    #find tradeable pais
    for market in markets.data["markets"].keys():
        market_info = markets.data["markets"][market]
        if market_info["status"] == "ONLINE" and market_info["type"] == "PERPETUAL":
            # print("market_info",market_info["market"])
            tradeable_markets.append(market)

    #set initial daateframe
    close_prices = get_candles_historical(client,tradeable_markets[0])
    df = pd.DataFrame(close_prices)
    df.set_index("datetime", inplace=True)


    #append other prices, to develop limit number
    for market in tradeable_markets[1:]:
      close_prices_add =get_candles_historical(client,market)
      df_add = pd.DataFrame(close_prices_add)
      df_add.set_index("datetime", inplace=True)
      df = pd.merge(df, df_add,how="outer",on="datetime",copy=False)
      del df_add

    #check any columns with NaNs
    nans= df.columns[df.isna().any()].tolist()
    if len(nans)>0:
      print("deleting nans")
      print(nans)
      df.drop(columns=nans,inplace=True)

    print(df)
    return df


if __name__ == "__main__":
    pass
    