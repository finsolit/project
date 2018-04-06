import requests
import json
from kucoin1.client import Client
def ask(pair,deep,deep1):
    payload = {'symbol':pair,'limit':'5','group':'1'}
    r = requests.get('https://api.kucoin.com/v1/open/orders',params=payload)
    r=r.json()
    kk=0
    rr=0
    for i in range(0,deep):
        kk=float(r['data']['BUY'][i][0])+kk
    kk=kk/deep
    for i in range(0,deep1):
        rr=float(r['data']['SELL'][i][0])+rr
    rr=rr/deep1
    return(kk,rr)
			
def order_sell(apikey,apisecret,ammount,symbol,price):
    client = Client(apikey, apisecret)	
    transaction = client.create_buy_order(symbol, price, ammount)
    return(transaction.orderOid,'1')
	
	
	
def order_buy(apikey,apisecret,ammount,symbol,price):
    client = Client(apikey, apisecret)	
    transaction = client.create_sell_order(symbol, price, ammount)
    return(transaction.orderOid,'1')
	


def cancel(symbol,id,orid,apikey,apisecret):
    client = Client(apikey, apisecret)	
    transaction = client.cancel_order(id)
	
def sum(apikey,apisecret,valet1,valet2):
    client = Client(apikey, apisecret)	
    transaction = client.get_all_balances()
    sum=0
    for i in range(0,len(transaction)):
        if transaction[i]['coinType']==valet1 or transaction[i]['coinType']==valet2:
            payload = {'fsym':transaction[i]['coinType'],'tsyms':'USD'}
            r = requests.get('https://min-api.cryptocompare.com/data/price',params=payload)
            r=r.json()
            sum=sum+(float(r['USD'])*float(transaction[i]['balance']))
    return(sum)