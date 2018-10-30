# -*- coding: utf-8 -*-
import os, sys, time, math
import re
import ccxt  # noqa: E402
from pprint import pprint
from styles import *
from process_pair import *


def print_usage():
    print_args("Usage: python " + sys.argv[0], green('id'), yellow('[symbol]'))
    print_args("Symbol is required, for example:")
    print_args("python " + sys.argv[0], green('gdax'), yellow('BTC/USD'))
    get_exchanges()


def print_exch_symbols(exchange):
    # output all symbols
    print_args(green(id), 'has', len(exchange.symbols), 'symbols:', yellow(', '.join(exchange.symbols)))


def get_exch_symbols(exchange):
    return exchange.symbols
    

def get_exchanges():
    return ccxt.exchanges


def get_ticker(exchange, symbol):
    try:        
        # get raw json data
        ticker = exchange.fetch_ticker(symbol.upper())

        print_args(
            green(exchange.id),
            yellow(symbol),
            'ticker',
            ticker['datetime'],
            'high: ' + str(ticker['high']),
            'low: ' + str(ticker['low']),
            'bid: ' + str(ticker['bid']),
            'ask: ' + str(ticker['ask']),
            'volume: ' + str(ticker['quoteVolume']))
        

    except ccxt.DDoSProtection as e:
        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        
    return ticker



###### unit tests ######

def test_ccxt_feed():
    try:
        id = sys.argv[1]  # get exchange id from command line arguments

        # check if the exchange is supported by ccxt
        exchange_found = id in ccxt.exchanges

        if exchange_found:
            print_args('Instantiating', green(id))

            # instantiate the exchange by id
            exchange = getattr(ccxt, id)()

            # load all markets from the exchange
            markets = exchange.load_markets()

            if len(sys.argv) > 2:  # if symbol is present, get that symbol only
                symbol = sys.argv[2]
                ticker = get_ticker(exchange, symbol) 
            else: 
                print_args('Symbol not found')
                print_exch_symbols(exchange)
                print_usage()

        else:
            print_args('Exchange ' + red(id) + ' not found')
            print_usage()

    except Exception as e:
        print(type(e).__name__, e.args, str(e))
        print_usage()



def test_exchange_list():
    supported_exchanges = get_exchanges()
    exch_list = ', '.join(str(name) for name in supported_exchanges)
    print(bold(underline('Supported exchanges: ')))
    pprint(exch_list, width=80)



if __name__ == '__main__':

#    test_exchange_list()
    test_ccxt_feed()
    

