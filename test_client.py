import logging
#from ibapi.wrapper import *
from ibapi.client import *
#from ibapi.contract import *
#from ibapi.order import *
#from threading import Thread
import queue
#import datetime
#import time
#import math


# Below is the TestClient/EClient class
class TestClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

    def server_clock(self):
        print('Asking server for Unix time')
        time_storage = self.wrapper.init_time()
        self.reqCurrentTime()
        max_wait_time = 10
        try:
            request_time = time_storage.get(timeout=max_wait_time)
        except queue.Empty:
            print('the queue is empty or max time reached')
            request_time = None
        while self.wrapper.is_error():
            print('Error')
            print(self.wrapper.get_error(timeout=5))
        return request_time

    def account_update(self):
        self.reqAccountSummary(9001, 'All', 'TotalCashValue, BuyingPower, AvailableFunds')

    def position_update(self):
        self.reqPositions()

    def price_update(self, contract, ticker_id):
        self.reqMktData(ticker_id, contract, '', False, False, [])
        return ticker_id
