# -*- coding: utf-8 -*-
import os
import sys
import time
import ccxt  # noqa: E402
from styles import green, yellow, blue, red, pink, bold, underline


def print_args(*args):
    print(' '.join([str(arg) for arg in args]))

def print_usage():
    print_args("Usage: python " + sys.argv[0], green('id'), yellow('[symbol]'))
    print_args("Symbol is required, for example:")
    print_args("python " + sys.argv[0], green('gdax'), yellow('BTC/USD'))
    get_exchanges()


def print_ticker(exchange, symbol):
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



def print_exch_symbols(exchange):
    # output all symbols
    print_args(green(id), 'has', len(exchange.symbols), 'symbols:', yellow(', '.join(exchange.symbols)))


def get_exchanges():
    return ccxt.exchanges


def get_exch_symbols(exchange):
    return exchange.symbols


def get_ticker(exchange, symbol):
    try:        
        print_ticker(exchange, symbol)
        # get raw json data
#        ticker = exchange.fetch_ticker(symbol.upper())
#        print(ticker)

    except ccxt.DDoSProtection as e:
        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        
        return ticker




if __name__ == '__main__':

    print("\n\n CCXT -------------------------------------\n\n")

#    supported_exchanges = 'Supported exchanges:', ', '.join(get_exchanges())
#    print(supported_exchanges)

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
                get_ticker(exchange, symbol)
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




