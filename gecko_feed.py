# Python imports
import requests, json, sys
from styles import green, yellow, blue, red, pink, bold, underline
import re

GECKO_COINS_URL = 'https://api.coingecko.com/api/v3/coins/'

"""To use Gecko API, first need to get coinlist in order search for base/quote individually
gecko does not provide pairs by default. for base/quote one must be listed as ticker
and the other lsited as full name, i.e. BTCUSD is vs_currency = usd , ids = bitcoin
https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin    
"""


isDebug = True

def debug(*args):
    if isDebug:
        print(' '.join([str(arg) for arg in args]))

def print_args(*args):
    print(' '.join([str(arg) for arg in args]))

def print_usage():
    print_args("Usage: python " + sys.argv[0], yellow('[symbol]'))
    print_args("Symbol is required, for example:")
    print_args("python " + sys.argv[0], yellow('BTC/USD'))


def get_gecko_json(url): 
    r = requests.get(url)
    json_obj = r.json()
    return json_obj
    

def check_gecko_symbol_exists(coinlist, symbol):    
    try:
        symbol_name = [obj for obj in coinlist if obj['symbol']==symbol][0]['id']
        return symbol_name
    except IndexError:
        return None
    

def filter_prefix_symbol(symbol):
    # example open.USD or bridge.USD, remove leading bit up to .
    base = ''
    if re.match(r'^[a-zA-Z](.*)\.(.*)', symbol):
        base = re.sub('(.*)\.', '', symbol)
    else:
        base = symbol
    return base


def filter_bit_symbol(symbol):
    # if matches bitUSD or bitusd any bit prefix, strip 
    base = ''
    if re.match(r'bit[a-zA-Z]{3}' , symbol):
        base = re.sub("bit", "", symbol)
    else:
        base = symbol
    return base


def get_gecko_market_price(base, quote):

    try:        
        coin_list = get_gecko_json(GECKO_COINS_URL+'list')
        quote_name = check_gecko_symbol_exists(coin_list, quote.lower())
        
        lookup_pair = "?vs_currency="+base.lower()+"&ids="+quote_name
        market_url = GECKO_COINS_URL+'markets'+lookup_pair
        print(market_url)
                
        ticker = get_gecko_json(market_url)
#        print("Getting ticker current price", ticker, sep='')

        for entry in ticker:
            current_price = entry['current_price']
            high_24h = entry['high_24h']
            low_24h = entry['low_24h']
            total_volume = entry['total_volume']
            
        return current_price

    except TypeError:
        return None


def split_pair(symbol):
    pair =  re.split(':|/', symbol)
    return pair


def test_split_symbol():
    try:
        group = ['BTC:USD', 'STEEM/USD']
        pair = [split_pair(symbol) for symbol in group]
        print('original:', group, 'result:',  pair, sep=' ')
    except Exception as e:
        pass


def test_gecko_pricefeed():
    '''base currency for coin gecko is in USD,EUR,JPY, CAD, etc, 
    see entire list here: https://api.coingecko.com/api/v3/global
    
    Example of no market = BTC/USDT
    Example of working market BTC/EUR or BTC/USD
    '''
    try:
        symbol = sys.argv[1]  # get exchange id from command line arguments

        pair = split_pair(symbol)

#        pair = [base, quote]
    
        filtered_pair = [filter_bit_symbol(j) for j in  [filter_prefix_symbol(i) for i in pair]]
        debug(filtered_pair)

        new_base = filtered_pair[0]
        new_quote = filtered_pair[1]

        current_price = get_gecko_market_price(new_base, new_quote)
        debug(current_price)
        
        if current_price is None:
            # try inverted version
            debug(" Trying pair inversion...")
            current_price = get_gecko_market_price(new_quote, new_base)
            # invert price
            debug(new_base+"/"+new_quote+ ":"+ str(current_price))
            if current_price is not None:
                actual_price = 1/current_price
                debug(new_quote+"/"+new_base+ ":"+ str(actual_price))


    except Exception as e:
        print(type(e).__name__, e.args, str(e))
        print_usage()



def test_filters():
    test_symbols = ['USDT', 'bridge.USD', 'Rudex.USD', 'open.USD', 
                    'GDEX.USD', 'Spark.USD', 'bridge.BTC', 'BTC', 'LTC', 
                    'bitUSD', 'bitEUR', 'bitHKD']

    print("Test Symbols", test_symbols, sep=":")
    
    r = [filter_prefix_symbol(i) for i in test_symbols]
    print("Filter prefix symbol", r, sep=":")

    r2 = [filter_bit_symbol(i) for i in r] 
    print("Apply to result, Filter bit symbol", r2, sep=":")



if __name__ == '__main__':

#    test_split_symbol()
#    test_filters()
    test_gecko_pricefeed()
