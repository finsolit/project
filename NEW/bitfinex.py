import requests
import json
import bitfinexpy

def ask(pair,deep,deep1):
    payload = {'limit_bids':'5','limit_asks':'5','group':'1'}
    r = requests.get('https://api.bitfinex.com/v1/book/'+pair,params=payload)
    r=r.json()
    kk=0
    rr=0
    for i in range(0,deep):
        kk=float(r['bids'][i]['price'])+kk
    kk=kk/deep
    for i in range(0,deep1):
        rr=float(r['asks'][i]['price'])+rr
    rr=rr/deep1
    return(kk,rr)
		
def order_sell(apikey,apisecret,ammount,symbol,price):
    bitfinex = bitfinexpy.API(environment="live", key=apikey, secret_key=apisecret)
    rr=bitfinex.new_order(symbol=symbol, amount=ammount, price=price, side="sell", type="limit")
    return(rr.id,'1')

	
	
	
def order_buy(apikey,apisecret,ammount,symbol,price):
    bitfinex = bitfinexpy.API(environment="live", key=apikey, secret_key=apisecret)
    rr=bitfinex.new_order(symbol=symbol, amount=ammount, price=price, side="buy", type="limit")
    return(rr.id,'1')	
	
def cancel(symbol,id,orid,apikey,apisecret):
    bitfinex = bitfinexpy.API(environment="live", key=apikey, secret_key=apisecret)
    bitfinex.cancel_order(order_id=id)    
	
	
	
	
def sum(apikey,apisecret,valet1,valet2):
    sum=0
    bitfinex = bitfinexpy.API(environment="live", key=apikey, secret_key=apisecret)
    rr=bitfinex.wallet_balances()
    for i in range(0,len(rr)):
        skr=str(rr[i]['currency']).upper()
        if skr==valet1 or skr==valet2:
            payload = {'fsym':skr,'tsyms':'USD'}
            r = requests.get('https://min-api.cryptocompare.com/data/price',params=payload)
            r=r.json()
            sum=sum+(float(r['USD'])*float(rr[i]['amount']))
    return(sum)