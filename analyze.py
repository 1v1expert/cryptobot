from api_wex import public_api, trade_api
import settings
# API Keys
api_key    = settings.API_KEY
api_secret = settings.API_SECRET
nonce      = 6

# Main
tapi = trade_api(api_key, api_secret, nonce)
info = tapi.getInfo()
if info['success']:
	funds = info['return']['funds']
	total = 0.00
	print('COIN   BALANCE     PRICE        VALUE')
	for coin in funds:
		if funds[coin]:
			balance = '{0:.2f}'.format(funds[coin])
			price   = '{0:.2f}'.format(public_api.ticker(coin, 'usd')[f'{coin}_usd']['sell'])
			value   = '{0:.2f}'.format(float(balance) * float(price))
			total += float(value)
			print('{0}{1}${2}${3}'.format(coin.ljust(7, ' '), balance.ljust(12, ' '), price.ljust(12, ' '), value))
	print('Total: ${0:.2f}'.format(total))
else:
	print('[!] Error - ' + info['error'])