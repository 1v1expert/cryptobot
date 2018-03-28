from api_wex import public_api, trade_api
from settings import *

# API Keys
api_key    = API_KEY
api_secret = API_SECRET
nonce      = 10

non_coin = ['rur', 'ethet', 'ruret']
# Main
tapi = trade_api(api_key, api_secret, nonce)
info = tapi.getInfo()
print(info)
if info['success']:
	funds = info['return']['funds']
	total = 0.00
	print('COIN   BALANCE     PRICE        VALUE')
	for coin in funds:
		if funds[coin] and coin not in non_coin:
			balance = '{0:.7f}'.format(funds[coin])
			if coin == 'usd':
				price = '{0:.1f}'.format(1.0)
			else:
				price   = '{0:.5f}'.format(public_api.ticker(coin, 'usd')[f'{coin}_usd']['sell'])
			value   = '{0:.5f}'.format(float(balance) * float(price))
			total += float(value)
			print('{0}{1}${2}${3}'.format(coin.ljust(7, ' '), balance.ljust(12, ' '), price.ljust(12, ' '), value))
	print('Total: ${0:.4f}'.format(total))
else:
	print('[!] Error - ' + info['error'])