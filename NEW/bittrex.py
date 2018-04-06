import requests
import json
from bittrex1 import *
from bittrex1 import Bittrex, API_V2_0



def ask(pair,deep,deep1):
    payload = {'market':pair,'type':'both'}
    r = requests.get('https://bittrex.com/api/v1.1/public/getorderbook',params=payload)
    r=r.json()
    kk=0
    rr=0
    for i in range(0,deep):
        kk=float(r['result']['buy'][i]['Rate'])+kk
    kk=kk/deep
    for i in range(0,deep1):
        rr=float(r['result']['sell'][i]['Rate'])+rr
    rr=rr/deep1
    return(kk,rr)
		
def order_sell(apikey,apisecret,ammount,symbol,price):
    my_bittrex = Bittrex(apikey, apisecret, api_version=API_V1_1) 
    tt=my_bittrex.sell_limit(symbol,ammount,price)
    return(tt['result']['uuid'],'1') 
       		
	
	
	
def order_buy(apikey,apisecret,ammount,symbol,price):
    my_bittrex = Bittrex(apikey, apisecret, api_version=API_V1_1) 
    tt=my_bittrex.buy_limit(symbol,ammount,price)
    return(tt['result']['uuid'],'1')
		
	
def cancel(symbol,id,orid,apikey,apisecret):
    my_bittrex = Bittrex(apikey, apisecret, api_version=API_V1_1) 
    tt=my_bittrex.cancel(id)   
		
		
		
		
def sum(apikey,apisecret,valet1,valet2):
    sum=0		
    my_bittrex = Bittrex(apikey, apisecret, api_version=API_V1_1)

    tt=my_bittrex.get_balance(valet1)
    bb=my_bittrex.get_balance(valet2)
    sum1=float(tt['result']['Balance'])
    sum2=float(bb['result']['Balance'])

    payload = {'fsym':valet1,'tsyms':'USD'}
    r = requests.get('https://min-api.cryptocompare.com/data/price',params=payload)
    r=r.json()
    sum=sum+(float(r['USD'])*float(sum1))
    payload = {'fsym':valet2,'tsyms':'USD'}
    r = requests.get('https://min-api.cryptocompare.com/data/price',params=payload)
    r=r.json()
    sum=sum+(float(r['USD'])*float(sum2))
    return(sum)