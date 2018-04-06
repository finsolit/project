import requests
import json
import threading
import time
import MySQLdb
import _pickle as pickle
import binance
import bitfinex
import bittrex
import kucoin
import okex
def servise(user_id,binance_work,bitfinex_work,bittrex_work,kucoin_work,okex_work,deep1,deep2,val,amount,percent):
    connection = MySQLdb.connect(
                    host = '136.243.151.88',
                    user = 'cryptobot',
                    passwd = 'Mmo2zBF8Vcy98QwRsvVJ')  # create the connection

    cursor = connection.cursor()     # get the cursor


    cursor.execute("USE cryptobot2") # select the database

    cursor.execute("select * from apikeys")    # execute 'SHOW TABLES' (but data is$
    tables = cursor.fetchall()       # return data from last query
    input = open('str.pkl', 'rb')
    users = pickle.load(input)
    input.close()  
#pairs_bitfinex=['tBCHETH','tBCHBTC']
#pairs_bittrex=['usdt-ada']
#pairs_okex=['btc_usd','etc_usd']
    limitnum=3
    apikey_list=['','','','','']
    secretkey_list=['','','','','']
    list_birj=['binance','bitfinex','bittrex','kucoin','okex']
    list_work=[binance_work,bitfinex_work,bittrex_work,kucoin_work,okex_work]
    price=0
    for k in range(0,5):
        if list_work[k]==1:
            for i in range(0,len(tables)):
                if tables[i][1]==user_id and tables[i][3]==list_birj[k]:	
                    apikey_list[k]=tables[i][4]
                    secretkey_list[k]=tables[i][5]	



    cursor.execute("USE cryptobot2") # select the database

    cursor.execute("select * from users")    # execute 'SHOW TABLES' (but data is$
    tables = cursor.fetchall()  
    
    if limitnum==-1:
        users.remove(user_id)
        output = open('str.pkl', 'wb')
        pickle.dump(users, output, 2)
        output.close()
        return()
    limits=[100,5000,30000,10000000000000000000000000000000000]
				
    bids=[0,0,0,0,0]
    asks=[0,0,0,0,0]



    def exch(val,percent):
        if val[0]!='' and apikey_list[0]!='' and list_work[0]!=0:
            t1 = threading.Thread(target=exch_binance, args=(val[0],))
            t1.start()
        if val[1]!='' and apikey_list[1]!='' and list_work[1]!=0:		
            t2 = threading.Thread(target=exch_bitfinex, args=(val[1],))
            t2.start()	
        if val[2]!='' and apikey_list[2]!='' and list_work[2]!=0:
            t3 = threading.Thread(target=exch_bittrex, args=(val[2],))
            t3.start()
        if val[3]!='' and apikey_list[3]!='' and list_work[3]!=0: 
            t4 = threading.Thread(target=exch_kucoin, args=(val[3],))
            t4.start()
        if val[4]!='' and apikey_list[4]!='' and list_work[4]!=0:
            t5 = threading.Thread(target=exch_okex, args=(val[4],))
            t5.start()    
		
        time.sleep(1)
        hb=0
        ha=0	
    #print(bids)
    #print(asks)
        while True:
            for i in range(0,4):
                if bids[i]!=0:
                    max=bids[i]
            for i in range(0,4):
                if asks[i]!=0:
                    min=asks[i]
            for i in range(0,len(bids)):
                if bids[i]>max and bids[i]!=0:
                    max=bids[i]
                    hb=i
                if asks[i]<min and asks[i]!=0:
                    min=asks[i]
                    ha=i
        #print('Max Bid= ',max,'Min Ask=',min)
            vigoda=(max-min)/max*100
            if vigoda > percent and hb!= ha:
                return(vigoda,hb,ha,max,min)
    


    def exch_binance(val):
            while True:
                a=binance.ask(val,deep1,deep2) 
    
                try:
                    bids[0]=float(a[0])
                    asks[0]=float(a[1])		
                except Exception:
                    bids[0]=0
                    asks[0]=0  
			
	
    def exch_bitfinex(val):
        while True:
            a=bitfinex.ask(val,deep1,deep2) 
            try:
                bids[1]=float(a[0])
                asks[1]=float(a[1])	
            except Exception:
                bids[1]=0
                asks[1]=0 	
			
			
    def exch_bittrex(val):
        while True:
            a=bittrex.ask(val,deep1,deep2)
            try:		
                bids[2]=float(a[0])
                asks[2]=float(a[1])
            except Exception:
                bids[2]=0
                asks[2]=0 
			
			
    def exch_kucoin(val):
        while True:
            a=kucoin.ask(val,deep1,deep2) 
            try:
                bids[3]=float(a[0])
                asks[3]=float(a[1])
            except Exception:
                bids[3]=0
                asks[3]=0 
			
			
    def exch_okex(val):
        while True:
            a=okex.ask(val,deep1,deep2) 
            try:
                bids[4]=float(a[0])
                asks[4]=float(a[1])
            except Exception:
                bids[4]=0
                asks[4]=0 
			
			
			
			
    USD_LTC=['LTCUSDT','ltcusd','usdt-ltc','LTC-USDT','ltc_usdt']
    ETH_LTC=['LTCETH','','eth-ltc','LTC-ETH','']
    LTC_BTC=['LTCBTC','ltcbtc','btc-ltc','LTC-BTC','ltc_btc']
    DASH_BTC=['DASHBTC','','btc-dash','DASH-BTC','']
    ETC_BTC=['ETCBTC','etcbtc','btc-etc','ETC-BTC','etc_btc']
    NEO_BTC=['NEOBTC','neobtc','btc-neo','','neo_btc']
    NEO_USD=['NEOUSDT','neousd','usdt-neo','','neo_usdt']
    DASH_ETH=['DASHETH','','eth-dash','DASH-ETH','']
    ZEC_ETH=['ZECETH','','eth-zec','','']
    NEO_ETH=['NEOETH','neoeth','eth-neo','','']
    ETH_USD=['ETHUSDT','ethusd','usdt-eth','','eth_usdt']
    ZEC_BTC=['ZECBTC','','btc-zec','','']
    XRP_BTC=['XRPBTC','xrpbtc','btc-xrp','','']
    XRP_ETH=['XRPETH','','eth-xrp','','']
    ADA_BTC=['ADABTC','','btc-ada','','']
    ADA_ETH=['ADAETH','','eth-ada','','']
    ZEC_USD=['','zecusd','usdt-zec','','']
    XRP_USD=['','xrpusd','usdt-xrp','','']
    BCH_USD=['','bchusd','','','bch_usdt']
    allpairs=[USD_LTC,ETH_LTC,LTC_BTC,DASH_BTC,ETC_BTC,NEO_BTC,NEO_USD,DASH_ETH,ZEC_ETH,NEO_ETH,ETH_USD,ZEC_BTC,XRP_BTC,XRP_ETH,ADA_BTC,ADA_ETH,ZEC_USD,XRP_USD,BCH_USD]
    allsymbol=['LTC-USDT','ETH-LTC','LTC-BTC','DASH-BTC','ETC-BTC','NEO-BTC','NEO-USD','DASH-ETH','ZEC-ETH','NEO-ETH','ETH-USDT','ZEC-BTC','XRP-BTC','XRP-ETH','ADA-BTC','ADA-ETH','ZEC-USD','XRP-USD','BCH-USDT']
    for i in range(0,len(allsymbol)):
        if allsymbol[i]==val:
            val=i
            for k in range(0,len(allsymbol[i])):
                if allsymbol[i][k]=='-':
                    valute1=allsymbol[i][:k]
                    valute2=allsymbol[i][k+1:]
            break

    list_sum=[binance.sum,bitfinex.sum,bittrex.sum,kucoin.sum,okex.sum]
    sum=0	
    for i in range(0,5):
        if apikey_list[i]!='' and list_work[i]!=0:
            sum=sum+list_sum[i](apikey_list[i],secretkey_list[i],valute1,valute2)


    if sum>limits[limitnum]:
        users.remove(user_id)
        output = open('str.pkl', 'wb')
        pickle.dump(users, output, 2)
        output.close()	
        return()		
		










    list_ask=[binance.ask,bitfinex.ask,bittrex.ask,kucoin.ask,okex.ask]
    list_sell=[binance.order_sell,bitfinex.order_sell,bittrex.order_sell,kucoin.order_sell,okex.order_sell]
    list_buy=[binance.order_buy,bitfinex.order_buy,bittrex.order_buy,kucoin.order_buy,okex.order_buy]
    list_cancel=[binance.cancel,bitfinex.cancel,bittrex.cancel,kucoin.cancel,okex.cancel]
    sinq=allpairs[val]
    print(allpairs[val])
    while True:
        input = open('str.pkl', 'rb')
        users = pickle.load(input)
        input.close() 
        if user_id not in users:
            return()
        vig=exch(allpairs[val],percent)
        bid1=vig[1]
        ask1=vig[2]
        max=vig[3]
        min=vig[4]
        vig=vig[0]
        if vig > percent:
            print(vig,'Bid',list_birj[bid1],'Ask',list_birj[ask1])
            getprof1=list_ask[bid1]
            getprof2=list_ask[ask1]
            try:
                getprof1=float(getprof1(sinq[bid1],deep1,deep2)[0])	
                getprof2=float(getprof2(sinq[ask1],deep1,deep2)[1])
            except Exception:
                getprof1=0
                getprof2=0
            vigoda=((getprof1)-(getprof2))/getprof1*100
            if vigoda>percent:
                print('proverka proidena')
                kk=list_buy[ask1]				
                #BUY=kk(apikey,apisecret,amount,allpairs[val][ask1],min)
                kk=list_sell[bid1]
                #SELL=kk(apikey,apisecret,amount,allpairs[val][bid1],max)
                print('ordera vistavleni')
                time.sleep(10)
                kk=list_cancel[ask1]
                #kk(allpairs[val][ask1],BUY[0],BUY[1],apikey,apisecret)
                kk=list_cancel[bid1]
                #kk(allpairs[val][bid1],SELL[0],SELL[1],apikey,apisecret)			
            else:	
                print('proverka ne proidena')		