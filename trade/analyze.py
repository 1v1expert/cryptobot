from api_wex import public_api, trade_api
from settings import *
import api_vk

# API Keys
api_key    = API_KEY
api_secret = API_SECRET
nonce      = 10

login = VK_LOGIN
password = VK_PASSWORD

def get_info_coins():
	non_coin = ['rur', 'ethet', 'ruret']
	# Main
	tapi = trade_api(api_key, api_secret, nonce)
	info = tapi.getInfo()
	msg = ''
	if info['success']:
		funds = info['return']['funds']
		total = 0.00
		msg += 'COIN   BALANCE     PRICE        VALUE\n'
		for coin in funds:
			if funds[coin] and coin not in non_coin:
				balance = '{0:.7f}'.format(funds[coin])
				if coin == 'usd':
					price = '{0:.1f}'.format(1.0)
				else:
					price   = '{0:.5f}'.format(public_api.ticker(coin, 'usd')[f'{coin}_usd']['sell'])
				value   = '{0:.5f}'.format(float(balance) * float(price))
				total += float(value)
				msg += '{0}{1}${2}${3}\n'.format(coin.ljust(7, ' '), balance.ljust(12, ' '), price.ljust(12, ' '), value)
		msg += 'Total: ${0:.4f}'.format(total)
	else:
		msg += '[!] Error - ' + info['error']
	return msg

if __name__=='__main__':
	vk_session = api_vk.VkApi(login, password)
	try:
		vk_session.auth()
	except api_vk.AuthError as error_msg:
		print(error_msg)
	vk = vk_session.get_api()
	response = vk.messages.send(domain='1v1expert', message=get_info_coins())