# -*- coding: utf-8 -*-
## Author:      VLADDOS
## e-mail:      sepstamp@mail.ru
## BTC   :      ---/
## donate free =)
#import http.client
#import urllib.request, urllib.parse, urllib.error
import settings

#http_timeout = 10

import hashlib
import hmac
import http.client
import json
import urllib.parse
import time

# Globals
http_timeout = 10

class public_api:
	def api_call(method):
		conn = http.client.HTTPSConnection('wex.nz', timeout=http_timeout)
		conn.request('GET', '/api/3/' + method)
		response = conn.getresponse().read().decode()
		data     = json.loads(response)
		conn.close()
		return data

	def info():
		return public_api.api_call('info')

	def ticker(tfrom, tto):
		return public_api.api_call(f'ticker/{tfrom}_{tto}')

	def depth(dfrom, dto, limit=None):
		if limit: # 150 Default / 5000 Max
			return public_api.api_call(f'depth/{dfrom}_{dto}?limit={limit}')
		else:
			return public_api.api_call(f'depth/{dfrom}_{dto}')

	def trades(dfrom, dto, limit=None):
		if limit: # 150 Default / 5000 Max
			return public_api.api_call(f'trades/{dfrom}_{dto}?limit={limit}')
		else:
			return public_api.api_call(f'trades/{dfrom}_{dto}')

class trade_api:
	def __init__(self, api_key, api_secret, api_nonce):
		self.api_key    = api_key
		self.api_secret = api_secret
		self.api_nonce  = api_nonce

	def signature(self, params):
		sig = hmac.new(self.api_secret.encode(), params.encode(), hashlib.sha512)
		return sig.hexdigest()

	def api_call(self, method, params):
		self.api_nonce = str(time.time()).split('.')[0]
		params['method'] = method
		params['nonce']  = str(self.api_nonce)
		params  = urllib.parse.urlencode(params)
		headers = {'Key':self.api_key, 'Sign':self.signature(params)}
		conn    = http.client.HTTPSConnection('wex.nz', timeout=http_timeout)
		conn.request('POST', '/tapi', params, headers)
		print(conn.source_address)
		response = conn.getresponse().read().decode()
		print(response)
		data = json.loads(response)
		conn.close()
		return data

	def getInfo(self):
		return self.api_call('/getInfo/', {})

	def Trade(self, tpair, ttype, trate, tamount):
		params = {'pair':tpair, 'type':ttype, 'rate':trate, 'amount':tamount}
		return self.api_call('Trade', params)

	def ActiveOrders(self, tpair=None):
		if tpair:
			params = {'pair':tpair}
			return self.api_call('ActiveOrders', params)
		else:
			return self.api_call('ActiveOrders', {})

	def OrderInfo(self, order_id):
		params = {'order_id':order_id}
		return self.api_call('OrderInfo', params)

	def CancelOrder(self, order_id):
		params = {'order_id':order_id}
		return self.api_call('CancelOrder', params)

	def TradeHistory(self, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend, tpair):
		params = {'from':tfrom, 'count':tcount, 'from_id':tfrom_id, 'end_id':tend_id, 'order':torder, 'since':tsince, 'end':tend, 'pair':tpair}
		return self.api_call('TradeHistory', params)

	def TransHistory(self, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend):
		params = {'from':tfrom, 'count':tcount, 'from_id':tfrom_id, 'end_id':tend_id, 'order':torder, 'since':tsince, 'end':tend}
		return self.api_call('TransHistory', params)

	def CoinDepositAddress(self, coinName):
		params = {'coinName':coinName}
		return self.api_call('CoinDepositAddress', params)

	def WithdrawCoin(self, coinName, amount, address): # Requires a special API key. See Trade API docs for more information.
		params = {'coinName':coinName, 'amount':amount, 'address':address}
		return self.api_call('WithdrawCoin', params)

	def CreateCoupon(self, currency, amount, receiver): # Requires a special API key. See Trade API docs for more information.
		params = {'currency':currency, 'amount':amount, 'receiver':receiver}
		return self.api_call('CreateCoupon', params)

	def RedeemCoupon(self, coupon): # Requires a special API key. See Trade API docs for more information.
		params = {'coupon':coupon}
		return self.api_call('RedeemCoupon', params)
