from api_wex import public_api, trade_api
from settings import *
import api_vk

# API Keys
api_key    = API_KEY
api_secret = API_SECRET
nonce      = 10

login = VK_LOGIN
password = VK_PASSWORD

class ProcessingWallet():
	def __init__(self):
		pass
	
	def get_assets(self, full):
		non_coin = ['rur', 'ethet', 'ruret']
		# Main
		tapi = trade_api(api_key, api_secret, nonce)
		info = tapi.getInfo()
		msg = ''
		if info['success']:
			funds = info['return']['funds']
			total = 0.00
			if full: msg += 'COIN   BALANCE     PRICE        VALUE\n'
			for coin in funds:
				if funds[coin] and coin not in non_coin:
					balance = '{0:.7f}'.format(funds[coin])
					if coin == 'usd':
						price = '{0:.1f}'.format(1.0)
					else:
						price   = '{0:.6f}'.format(public_api.ticker(coin, 'usd')[f'{coin}_usd']['sell'])
					value   = '{0:.6f}'.format(float(balance) * float(price))
					total += float(value)
					if full: msg += '{0}{1}${2}${3}\n'.format(coin.ljust(7, ' '), str(round(float(balance), 4)).ljust(12, ' '), str(round(float(price), 2)).ljust(12, ' '), round(float(value), 2))
			msg += 'Total: ${0:.5f}'.format(total)
		else:
			msg += '[!] Error - ' + info['error']
		return msg
	
	def get_rank(self):
		pass
	
if __name__=='__main__':
	vk_session = api_vk.VkApi(login, password)
	try:
		vk_session.auth()
	except api_vk.AuthError as error_msg:
		print(error_msg)
	vk = vk_session.get_api()
	response = vk.messages.send(domain='1v1expert', message=ProcessingWallet().get_assets(False))