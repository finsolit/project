import requests
import json
import time
from okex1.client import OKCoinSpot
def ask(pair,deep,deep1):
    r = requests.get('https://www.okex.com/api/v1/depth.do?symbol='+pair)
    r=r.json()
    kk=0
    rr=0
    for i in range(0,deep):
        kk=float(r['bids'][i][0])+kk
    kk=kk/deep
    for i in range(0,deep1):
        zz=len(r['asks'])-1
        rr=float(r['asks'][zz-i][0])+rr
    rr=rr/deep1
    return(kk,rr)
		
		
def order_sell(apikey,apisecret,ammount,symbol,price):
    secretkey=apisecret
    okcoinRESTURL = 'www.okex.com'
    okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)
    r=okcoinSpot.trade(symbol,'sell',price,ammount)
    r=json.loads(r)
    return(r['order_id'],symbol)
	
	
	
def order_buy(apikey,apisecret,ammount,symbol,price):
    secretkey=apisecret
    okcoinRESTURL = 'www.okex.com'
    okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)
    r=okcoinSpot.trade(symbol,'buy',price,ammount)
    r=json.loads(r)
    return(r['order_id'],symbol)

def cancel(symbol,id,orid,apikey,apisecret):
    secretkey=apisecret
    okcoinRESTURL = 'www.okex.com'
    okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)
    r=okcoinSpot.cancelOrder(symbol,id)
		
		
		
def sum(apikey,apisecret,valet1,valet2):
    sum=0
    secretkey=apisecret
    okcoinRESTURL = 'www.okex.com'
    okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)
    r=okcoinSpot.userinfo()
    r=json.loads(r)
    z=list(r['info']['funds']['borrow'].keys())
    skr=str(z[0]).upper()
    for i in range(0,len(r['info']['funds']['borrow'])):
        skr=str(z[i]).upper()
        if skr==valet1 or skr==valet2:
            payload = {'fsym':skr,'tsyms':'USD'}
            r1 = requests.get('https://min-api.cryptocompare.com/data/price',params=payload)
            r1=r1.json()
            sum=sum+(float(r['info']['funds']['borrow'][z[i]])*float(r1['USD']))

    z=list(r['info']['funds']['free'].keys())
    skr=str(z[0]).upper()
    for i in range(0,len(r['info']['funds']['free'])):
        skr=str(z[i]).upper()
        if skr==valet1 or skr==valet2:
            payload = {'fsym':skr,'tsyms':'USD'}
            r1 = requests.get('https://min-api.cryptocompare.com/data/price',params=payload)
            r1=r1.json()
            sum=sum+(float(r['info']['funds']['free'][z[i]])*float(r1['USD']))
		
		
    z=list(r['info']['funds']['freezed'].keys())
    skr=str(z[0]).upper()
    for i in range(0,len(r['info']['funds']['freezed'])):
        skr=str(z[i]).upper()
        if skr==valet1 or skr==valet2:
            payload = {'fsym':skr,'tsyms':'USD'}
            r1 = requests.get('https://min-api.cryptocompare.com/data/price',params=payload)
            r1=r1.json()
            sum=sum+(float(r['info']['funds']['freezed'][z[i]])*float(r1['USD']))
    return(sum)