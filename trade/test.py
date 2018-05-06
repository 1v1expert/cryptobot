from api_wex import public_api, trade_api
from settings import *
import api_vk
import csv
import random

# API Keys
api_key    = API_KEY
api_secret = API_SECRET
nonce      = 10

login = VK_LOGIN
password = VK_PASSWORD

BALANCE = 150
KOEF = 1.01

coins = ['btc', 'ltc', 'nmc', 'nvc', 'ppc', 'dsh', 'eth', 'bch', 'zec']

def get_rank_pair(coin):
    coinf_info = public_api.ticker(coin, 'usd')[f'{coin}_usd']
    RANK = ((coinf_info['buy'] - coinf_info['sell'])/coinf_info['sell']) * coinf_info['vol_cur']
    return RANK

def put_number():
    # необходимо производить нумерацию обращений для того, чтобы была возможность получать статистику за последние промежутки времени
    try:
        file = open('info.csv')
    except IOError as e:
        with open('info.csv', 'a+') as file:
            data = [1, BALANCE]
            writer = csv.writer(file, delimiter=';')
            writer.writerow(data)
            return 1
    else:
        with file:
            reader = csv.DictReader(file, delimiter=';')
            for line in reader:
                pass
            num = int(line['num'])
            bal = float(line['bal'])
            file.close()
            
        with open('info.csv', 'a+') as file:
            data = [num+1, bal]
            writer = csv.writer(file, delimiter=';')
            writer.writerow(data)
        return num
        
def logging():
    # собираем статистику по монетам в отдельный для каждой монеты файл
    num = put_number()
    for coin in coins:
        path, rank = coin + '_info.csv', '{0:.1f}'.format(get_rank_pair(coin))
        buy = public_api.ticker(coin, 'usd')[f'{coin}_usd']['buy']
        sel = public_api.ticker(coin, 'usd')[f'{coin}_usd']['sell']
        vol = public_api.ticker(coin, 'usd')[f'{coin}_usd']['vol_cur']
        avg = public_api.ticker(coin, 'usd')[f'{coin}_usd']['avg']
        data = [num, rank, buy, sel, vol, avg]
        with open(path, 'a+') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(data)
            
def get_max_rating():
    rank = 0.0
    max_coin = None
    for coin in coins:
        path = coin + '_info.csv'
        with open(path) as file:
            reader = csv.DictReader(file, delimiter=';')
            for line in reader:
                pass
            if float(line['rank']) > rank:
                rank = float(line['rank'])
                max_coin = coin
    return max_coin, rank

def get_randomize_num():
    return random.randrange(10234, 99999, 1)

def initialization():
    # создаём и заполняем файлы при инициализации
    info = ['num', 'bal']
    with open('info.csv', 'a+') as inf_file:
        writer = csv.writer(info, delimiter=';')
        writer.writerow(info)
        
    data_info = ['num', 'rank', 'buy', 'sel', 'vol', 'avg']
    
    for coin in coins:
        path = coin + '_info.csv'
        with open(path, 'a+') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(data_info)
            
    data_tranzaction = ['num', 'coin', 'price', 'count']
    # отдельные файлы транзакций на покупку и продажу
    with open('tranzactions_sell.csv', 'a+') as tr_file:
        writer = csv.writer(tr_file, delimiter=';')
        writer.writerow(data_tranzaction)
        
    with open('tranzactions_buy.csv', 'a+') as tr_file:
        writer = csv.writer(tr_file, delimiter=';')
        writer.writerow(data_tranzaction)
        
def check_orders():
    # формируем список из содержимого файлов
    tranzactions_buy = []
    with open('tranzactions_buy.csv') as tr_file:
        reader = csv.DictReader(tr_file, delimiter=';')
        for line in reader:
            tranzactions_buy.append(line)
    tranzactions_sell = []
    
    with open('tranzactions_sell.csv') as tr_file:
        reader = csv.DictReader(tr_file, delimiter=';')
        for line in reader:
            tranzactions_sell.append(line)
    # пробегаемся по номерам транзакций и ищем незакрытые транзакции
    for tranzact_buy in tranzactions_buy:
        close = False
        for tranzact_sell in tranzactions_sell:
            if int(tranzact_buy['num']) == int(tranzact_sell['num']):
                close = True
                break
        # если есть открытая транзакция, то передаём данные в check_tranzact на проверку исполненности ордера
        if not close: check_tranzact(tranzact_buy['num'], tranzact_buy['coin'], tranzact_buy['price'])
        
def check_tranzact(num, coin, price):
    # проверяем не исполнился ли наш ордер
    current_price = public_api.ticker(coin, 'usd')[f'{coin}_usd']['sell']
    if current_price >= (float(price)*KOEF):
        put_tranzact(False, num, coin, current_price)
        
def put_tranzact(type, num, coin, price):
    if not type:
        with open('tranzactions_sell.csv', 'a+') as file:
            data = [num, coin, price]
            writer = csv.writer(file, delimiter=';')
            writer.writerow(data)
    else:
        with open('tranzactions_sell.csv', 'a+') as file:
            data = [num, coin, price]
            writer = csv.writer(file, delimiter=';')
            writer.writerow(data)

def buy_coins():
    pass

def output_statistics():
    pass

def first_start():
    # проверка на существование файлов необходимо при первом запуске
    try:
        num_file = open('info.csv')
        trunz_sell_file = open('tranzactions_sell.csv')
        trunz_buy_file = open('tranzactions_buy.csv')
        info_file = open('btc_info.csv')
    except IOError as e:
        initialization()
    else:
        with num_file:
            num_file.close()
        with trunz_sell_file:
            trunz_sell_file.close()
        with trunz_buy_file:
            trunz_buy_file.close()
        with info_file:
            info_file.close()
        working_cicle()
        
def working_cicle():
    logging() # собираем данные по монетам
    check_orders() # проверяем транзакции
    buy_coins()
    output_statistics()
    
if __name__=='__main__':
    pass