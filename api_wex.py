# -*- coding: utf-8 -*-
## Author:      VLADDOS
## e-mail:      sepstamp@mail.ru
## BTC   :      ---/
## donate free =)
import http.client
import urllib.request, urllib.parse, urllib.error
import json
import hashlib
import hmac

http_timeout = 10

class public_api:
  def api_call(self, method):
    conn = http.client.HTTPSConnection('wex.nz', timeout=http_timeout)
    conn.request('GET', '/api/3/' + method)
    response = conn.getresponse().read().decode()
    data     = json.loads(response)
    conn.close()
    return data

  def info(self):
    return public_api.api_call('info')

  def ticker(self, tfrom, tto):
    return self.public_api.api_call('ticker/{tfrom}_{tto}')

  def depth(self, dfrom, dto, limit=None):
    if limit: # 150 Default / 5000 Max
      return self.public_api.api_call('depth/{dfrom}_{dto}?limit={limit}')
    else:
      return self.public_api.api_call('depth/{dfrom}_{dto}')

  def trades(self, dfrom, dto, limit=None):
    if limit: # 150 Default / 5000 Max
      return self.public_api.api_call('trades/{dfrom}_{dto}?limit={limit}')
    else:
      return self.public_api.api_call('trades/{dfrom}_{dto}')

class trade_api:
  def __init__(self):
    self.ft = f.safe_date()
    self.api_key    = 'WNEP2NHW-AEHRXUHU-N3WTY47B-WW3K29MD-AL1IGMYQ'
    self.api_secret = '308a0bbbcbf7061d134c5a682a74feaef0d14b5484a25b23e0c15c5670a1ad0a'
    self.api_nonce  = self.ft.load_nonce()

  def __del__(self):
    pass

  def signature(self, params):
    sig = hmac.new(self.api_secret.encode(), params.encode(), hashlib.sha512)
    return sig.hexdigest()

  def api_call(self, method, params):
    #self.api_nonce = str(time.time()).split('.')[0]


    params['method'] = method
    params['nonce']  = str(self.api_nonce)
    params  = urllib.parse.urlencode(params)
    headers = {'Content-type':'application/x-www-form-urlencoded', 'Key':self.api_key, 'Sign':self.signature(params)}
    conn    = http.client.HTTPSConnection('wex.nz', timeout=http_timeout)
    conn.request('POST', '/tapi', params, headers)
    response = conn.getresponse().read().decode()
    data     = json.loads(response)
    conn.close()

    #self.api_nonce = int(self.api_nonce) + 1
    #self.non = int(self.api_nonce)
    #self.non += 1
    
    self.ft.save_nonce(self.api_nonce)
    return data

  def getInfo(self):
    #Info by
    self.api_nonce = int(self.api_nonce) + 1
    return self.api_call('getInfo', {})

  def Trade(self, tpair, ttype, trate, tamount):
    params = {'pair':tpair, 'type':ttype, 'rate':trate, 'amount':tamount}
    return self.api_call('Trade', params)

  def ActiveOrders(self, tpair=None):
    self.api_nonce = int(self.api_nonce) + 1
    if tpair:
      params = {'pair':tpair}
      return self.api_call('ActiveOrders', params)
    else:
      return self.api_call('ActiveOrders', {})

  def OrderInfo(self, order_id):
    self.api_nonce = int(self.api_nonce) + 1
    params = {'order_id':order_id}
    return self.api_call('OrderInfo', params)

  def CancelOrder(self, order_id):
    params = {'order_id':order_id}
    return self.api_call('CancelOrder', params)

  def TradeHistory(self, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend, tpair):
    params = {'from':tfrom, 'count':tcount, 'from_id':tfrom_id, 'end_id':tend_id, 'order':torder, 'since':tsince, 'end':tend, 'pair':tpair}
    return self.api_call('TradeHistory', params)

  def TransHistory(self, tfrom=None, tcount=None, tfrom_id=None, tend_id=None, torder=None, tsince=None, tend=None):
    self.api_nonce = int(self.api_nonce) + 1
    params = {'from':tfrom, 'count':tcount, 'from_id':tfrom_id, 'end_id':tend_id, 'order':torder, 'since':tsince, 'end':tend}
    return self.api_call('TransHistory', {})

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



'''if __name__ == '__main__':
  fircls = trade_api('WNEP2NHW-AEHRXUHU-N3WTY47B-WW3K29MD-AL1IGMYQ', '308a0bbbcbf7061d134c5a682a74feaef0d14b5484a25b23e0c15c5670a1ad0a', 1506691380)
  print(json.dumps(fircls.getInfo(), indent = 3, sort_keys = True ))
  print('Active Orders\n\n -------------------\n')
  print(json.dumps(fircls.ActiveOrders(), indent = 3, sort_keys = True ))
'''

