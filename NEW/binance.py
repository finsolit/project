import requests
import json
import time
from binclient import BinanceRESTAPI, BinanceWebSocketAPI

def ask(pair,deep,deep1):
    payload = {'symbol': pair,'limit':'5'}
    r = requests.get('https://api.binance.com/api/v1/depth',params=payload)
    r=r.json()
    kk=0
    rr=0
    for i in range(0,deep):
        kk=float(r['bids'][i][0])+kk
    kk=kk/deep
    for i in range(0,deep1):
        rr=float(r['asks'][i][0])+rr
    rr=rr/deep1
    return(kk,rr)

def order_sell(apikey,apisecret,ammount,symbol,price):
    rest_client = BinanceRESTAPI(apikey, apisecret)
    ws_client = BinanceWebSocketAPI(apikey)
    order = rest_client.new_order(symbol, "SELL", "LIMIT", "GTC", ammount, price,int(time.time()))
    return(order.id,order.client_order_id)
	
	
	
def order_buy(apikey,apisecret,ammount,symbol,price):
    rest_client = BinanceRESTAPI(apikey, apisecret)
    ws_client = BinanceWebSocketAPI(apikey)
    order = rest_client.new_order(symbol, "BUY", "LIMIT", "GTC", ammount, price,int(time.time()))
    return(order.id,order.client_order_id)

	
def cancel(symbol,id,orid,apikey,apisecret):
    rest_client = BinanceRESTAPI(apikey, apisecret)
    ws_client = BinanceWebSocketAPI(apikey)
    order = rest_client.cancel_order(symbol, id, orid,int(time.time()))
	
	
	
def sum(apikey,apisecret,valet1,valet2):
    rest_client = BinanceRESTAPI(apikey, apisecret)
    ws_client = BinanceWebSocketAPI(apikey)
    order = rest_client.account(int(time.time()))
    for i in range(0,len(order.balances)):
        asset=order.balances[i].asset
        free=order.balances[i].free
        if asset==valet1 or asset==valet2:
            payload = {'fsym':asset,'tsyms':'USD'}
            r = requests.get('https://min-api.cryptocompare.com/data/price',params=payload)
            r=r.json()
            sum=sum+(float(r['USD'])*float(free))
    return(sum)