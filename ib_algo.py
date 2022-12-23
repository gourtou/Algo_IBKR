import logging
from ibapi.wrapper import *
from ibapi.client import *
from ibapi.contract import *
from ibapi.order import *
from threading import Thread
import queue
import datetime
import time
import math
from test_wrapper import *
from test_client import *


# Global variables
AVAILABLE_FUNDS = 0
BUYING_POWER = 0
POSITIONS = {}
PRICE = 1000000


# Below are the custom classes and methods
def contract_create(symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.currency = "USD"
    contract.exchange = "SMART"
    contract.primaryExchange = "ISLAND"     # primary exchange
    return contract


def order_create():
    order = Order()
    order.action = 'BUY'
    order.orderType = 'MKT'
    order.transmit = True
    order.totalQuantity = 10    # quantity to buy/sell
    return order


def order_execution(symbol):
    contract = contract_create(symbol)
    order = order_create()
    next_id = app.next_order_id()
    time.sleep(2)
    print('ticker', contract.symbol, 'price:', PRICE)

    print('Next valid id:' + str(next_id))
    print('Buying Power:' + str(BUYING_POWER))
    print('Available Funds:' + str(AVAILABLE_FUNDS))

    app.placeOrder(next_id, contract, order)
    print('order placed with id', next_id)


def print_positions():
    for key, value in POSITIONS.items():
        symbol = key
        quantity = value['positions']
        cost = value['average cost']
        print(symbol, quantity, cost)
    return


# Below is the TestApp
class TestApp(TestWrapper, TestClient):
    def __init__(self, ip_address, port_id, client_id):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)
        self.connect(ip_address, port_id, client_id)

        # initialize the threading
        thread = Thread(target=self.run)
        thread.start()
        setattr(self, "_thread", thread)

        # start listening for errors
        self.init_error()


# Below is the program execution
if __name__ == '__main__':
    print('starting...')
    app = TestApp('127.0.0.1', 7497, 0)  # IP address, port (7496 for real, 7497 - for paper), clientId
    print('the program has begun')
    requested_time = app.server_clock()
    print('current server time', requested_time)
    app.account_update()
    app.position_update()
    for i in range(2):
        time.sleep(2)
        #order_execution()
        print_positions()



    # app.disconnect()

# Below is the input area


# Below is the logic processing area
