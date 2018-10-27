import asyncio
import aiohttp

# docs
# Gecko
# CCXT
# Waves
# Cryptowat.ch  https://cryptowat.ch/docs/api#pairs-index

gecko_coins_url = 'https://api.coingecko.com/api/v3/coins/'
waves_symbols = 'http://marketdata.wavesplatform.com/api/symbols'
cwatch_pairs='https://api.cryptowat.ch/pairs'

urls = [cwatch_agg_summaries, waves_symbols, gecko_coins_url]

@asyncio.coroutine
def call_url(url):
    print('Starting {}'.format(url))
    response = yield from aiohttp.ClientSession().get(url)
    data = yield from response.text()
    print('{}: {} bytes: {}'.format(url, len(data), data))    
    return data



futures = [call_url(url) for url in urls]

asyncio.run(asyncio.wait(futures))
