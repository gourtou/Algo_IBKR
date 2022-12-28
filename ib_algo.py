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
from scraper import *


# Global variables
AVAILABLE_FUNDS = 0
BUYING_POWER = 0
POSITIONS = {}
PRICE = 1000000
PRICE_BOOL = False
CYCLE = 12       # frequency of server requests
TEXTS = []
POSITIVE = ['exceeds', 'beats', 'apple', 'expectations']
NEGATIVE = ['drops', 'down']


# Below are the custom classes and methods
def contract_create(symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.currency = "USD"
    contract.exchange = "SMART"
    contract.primaryExchange = "ISLAND"     # primary exchange
    return contract


def order_create(quantity=1):
    order = Order()
    if quantity >=0:
        order.action = 'BUY'
        order.totalQuantity = quantity
    else:
        order.action = 'SELL'
        order.totalQuantity = -1 * quantity
    order.orderType = 'MKT'
    order.transmit = True
    return order


def order_execution(symbol):
    contract = contract_create(symbol)
    app.price_update(contract, app.next_order_id())
    next_id = app.next_order_id()
    print('ticker', contract.symbol, 'price:', PRICE)
    global PRICE_BOOL
    while not PRICE_BOOL:
        time.sleep(0.2)
    print('Next valid id:' + str(next_id))
    print('Buying Power:' + str(BUYING_POWER))
    print('Available Funds:' + str(AVAILABLE_FUNDS))

    order = order_create(quantity_to_buy())
    app.placeOrder(next_id, contract, order)
    PRICE_BOOL = False
    print('order placed with id', next_id)
    close_orders()


def close_orders():
    time.sleep(1195)
    app.position_update()
    time.sleep(5)
    for key, value in POSITIONS.items():
        symbol = key
        quantity = value['positions']
        cost = value['average cost']
        order_execution_normalize(symbol, -1 * quantity)

    print('position normalized')


def order_execution_normalize(symbol, quantity):
    contract = contract_create(symbol)
    order = order_create(quantity)
    next_id = app.next_order_id()
    app.placeOrder(next_id, contract, order)
    print('positions normalized')


def print_positions():
    for key, value in POSITIONS.items():
        symbol = key
        quantity = value['positions']
        cost = value['average cost']
        print(symbol, quantity, cost)
    return


def quantity_to_buy():
    return math.floor(BUYING_POWER/PRICE*0.01)      # 1% of buying power


def scrape():
    stock = 'AAPl'
    headline_holder = []
    search_economist(headline_holder)
    search_seekingalpha(headline_holder)
    search_cnn(headline_holder)
    search_reuters(headline_holder)
    for entry in headline_holder:
        print(entry)
        result = headline_analysis(entry)
        if result != 'no_change':
            order_execution(stock)
            return result
    time.sleep(randint(1, 5))
    return 'no_change'


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
    time.sleep(3)
    order_execution(stock)

    print_positions()

    while True:
        scrape()





    # app.disconnect()

# Below is the input area


# Below is the logic processing area
