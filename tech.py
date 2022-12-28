from ta import volatility
from ibapi import client
# from test_wrapper import *
from test_client import *
from datetime import datetime
import pytz
from pandas import DataFrame
import math
import yfinance as yf


# functions for technical analysis
# def indicators(stock):
    # atr_long = volatility.average_true_range(high, low, close, 60)

# add indicators
def format_dataframe(raw_dataframe):
    df = DataFrame()
    df.insert(0, 'Datetime', raw_dataframe.Datetime)
    df.insert(1, 'Open', raw_dataframe.Open)
    df.insert(2, 'High', raw_dataframe.High)
    df.insert(3, 'Low', raw_dataframe.Low)
    df.insert(4, 'Close', raw_dataframe.Close)
    df.insert(5, 'Volume', raw_dataframe.Volume)
    return df


def contract_create(symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.currency = "USD"
    contract.exchange = "SMART"
    contract.primaryExchange = "NYSE"     # primary exchange
    return contract


if __name__ == '__main__':
    print('start ta')
    contract = contract_create('BA')
    time_str = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y%m%d %H:%M:%S')
    time_for_histdata = datetime.strptime(time_str, '%Y%m%d %H:%M:%S')
    # data = client.EClient.reqHistoricalData(contract, time_for_histdata.strftime('%Y%m%d %H:%M:%S US/Eastern'), '5 D', '1 hour', 'TRADES', True, 1, keepUpToDate=False)
    ticker = yf.Ticker('BA')
    raw_data = ticker.history('1mo', '15m')
    raw_data.index.rename('Datetime', inplace=True)
    print(raw_data)

    #


