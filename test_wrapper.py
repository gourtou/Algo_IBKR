import logging
from ibapi.wrapper import *
from ibapi.client import *
#from ibapi.contract import *
#from ibapi.order import *
#from threading import Thread
import queue
#import datetime
#import time
#import math


# Below is the TestWrapper/EWrapper class
class TestWrapper(EWrapper):
    def __init__(self):
        super().__init__()
        self.my_errors_queue = queue.Queue()
        self.my_time_queue = queue.Queue()
        self.next_valid_order_id = 1

    # message handling methods (IB API returns all messages to client as errors)
    def init_error(self):
        error_queue = queue.Queue()
        self.my_errors_queue = error_queue

    def is_error(self):
        error_exist = not self.my_errors_queue.empty()
        return error_exist

    def get_error(self, timeout=3):
        if self.is_error():
            try:
                return self.my_errors_queue.get(timeout=timeout)
            except queue.Empty:
                return None
        return None

    def error(self, ticker_id, error_code, error_string):  # override
        error_message = "IB returns an error %d error code %d that says %s" % (ticker_id, error_code, error_string)
        self.my_errors_queue.put(error_message)

    # time handling methods
    def init_time(self):
        time_queue = queue.Queue()
        self.my_time_queue = time_queue
        return time_queue

    def currentTime(self, server_time):     # override
        self.my_time_queue.put(server_time)

    def nextValidId(self, order_id):        # override
        super().nextValidId(order_id)
        logging.debug('setting nextValidId:', order_id)
        self.next_valid_order_id = order_id

    def next_order_id(self):
        valid_order_id = self.next_valid_order_id
        self.next_valid_order_id += 1
        return valid_order_id

    def accountSummary(self, req_id, account, tag, value, currency):
        super().accountSummary(req_id, account, tag, value, currency)
        print('account', req_id, account, tag, value, currency)
        if tag == 'AvailableFunds':
            global AVAILABLE_FUNDS
            AVAILABLE_FUNDS = value
        if tag == 'BuyingPower':
            global BUYING_POWER
            BUYING_POWER = value

    def accountSummaryEnd(self, req_id):
        super().accountSummaryEnd(req_id)
        print('account summary ended', req_id)

    def position(self, account, contract, position, avg_cost):
        super().position(account, contract, position, avg_cost)
        global POSITIONS
        POSITIONS[contract.symbol] = {'position': position, 'average cost': avg_cost}
