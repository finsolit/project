import time
import threading
import _pickle as pickle
import main
import MySQLdb
import json
import binance
import bitfinex
import bittrex
import kucoin
import okex
users=[]
potoki=[]
was=[]
now=[]
connection = MySQLdb.connect(
                host = '127.0.0.1',
                user = 'cryptobot',
                passwd = 'Mmo2zBF8Vcy98QwRsvVJ')  # create the connection

cursor = connection.cursor()     # get the cursor


cursor.execute("USE cryptobot2") # select the database

cursor.execute("select * from strategies ")    # execute 'SHOW TABLES' (but data is$
tables = cursor.fetchall()
for i in range(0,len(tables)):
    sar=json.loads(tables[i][4])       # return data from last query
    print(tables[i][1],sar['binance'],sar['bitfinex'],sar['bittrex'],sar['kucoin'],sar['okex'],tables[i][6],tables[i][5],tables[i][3],tables[i][7],tables[i][9])
    was.append(tables[i][10])


def start(user_id,binance_work,bitfinex_work,bittrex_work,kucoin_work,okex_work,deep1,deep2,val,amount,percent,users):
        users.append(user_id)
        output = open('str.pkl', 'wb')
        pickle.dump(users, output, 2)
        output.close()
        potoki.append(threading.Thread(target=main.servise, args=(user_id,binance_work,bitfinex_work,bittrex_work,kucoin_work,okex_work,deep1,deep2,val,amount,percent,)))
        potoki[-1].start()
        time.sleep(5)
        input = open('str.pkl', 'rb')
        users = pickle.load(input)
        input.close()      
        if user_id in users	:	
            return ('Yes')
        return('No')	


def stop(user_id,users):
        for i in range(0,len(users)):
            if users[i] == user_id:
                z=i
        users.remove(user_id)
        output = open('str.pkl', 'wb')
        pickle.dump(users, output, 2)
        output.close()
        del  potoki[z]
        return {'Yes'}


		
		
def valuess(user_id,val,list_work,zz):
    connection = MySQLdb.connect(
                    host = '136.243.151.88',
                    user = 'cryptobot',
                    passwd = 'Mmo2zBF8Vcy98QwRsvVJ')  # create the connection

    cursor = connection.cursor()     # get the cursor


    cursor.execute("USE cryptobot2") # select the database

    cursor.execute("select * from apikeys")    # execute 'SHOW TABLES' (but data is$
    tables = cursor.fetchall()       # return data from last query
    apikey_list=['','','','','']
    secretkey_list=['','','','','']
    price=0
    list_birj=['binance','bitfinex','bittrex','kucoin','okex']
    for k in range(0,5):
        if list_work[k]==1:
            for i in range(0,len(tables)):
                if tables[i][1]==user_id and tables[i][3]==list_birj[k]:	
                    apikey_list[k]=tables[i][4]
                    secretkey_list[k]=tables[i][5]		

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
    if zz==1:		
        cursor.execute("UPDATE balances SET pair_to=%s, pair_from=%s WHERE user_id=%s",(str(sum),str(sum),user_id)) 
    if zz==0:
        cursor.execute("INSERT INTO balances VALUES pair_to=%s, pair_from=%s, user_id=%s",(str(sum),str(sum),user_id))        	
    
while True:
    time.sleep(5)
    now=[]
    connection = MySQLdb.connect(
                host = '136.243.151.88',
                user = 'cryptobot',
                passwd = 'Mmo2zBF8Vcy98QwRsvVJ')  # create the connection

    cursor = connection.cursor()     # get the cursor


    cursor.execute("USE cryptobot2") # select the database

    cursor.execute("select * from strategies ")    # execute 'SHOW TABLES' (but data is$
    tables = cursor.fetchall()
    for i in range(0,len(tables)):
        sar=json.loads(tables[i][4])       # return data from last query
        print(tables[i][1],sar['binance'],sar['bitfinex'],sar['bittrex'],sar['kucoin'],sar['okex'],tables[i][6],tables[i][5],tables[i][3],tables[i][7],tables[i][9])
        tk=[]
        tk=[int(sar['binance']),int(sar['bitfinex']),int(sar['bittrex']),int(sar['kucoin']),int(sar['okex'])]
                    
        cursor.execute("select * from balances")    # execute 'SHOW TABLES' (but data is$
        tables1 = cursor.fetchall()
        rorka=0
        for k in range(0,len(tables1)):
            if tables[i][1] == tables[k][1]:
                valuess(tables[i][1],tables[i][3],tk,1)		
                rorka=1				
                break
        if rorka==0:
            valuess(tables[i][1],tables[i][3],tk,0)			
        now.append(tables[i][10]) 
    for i in range (0,len(was)):
        sar=json.loads(tables[i][4])
        if now[i]!=was[i]:
            if now[i]=='0':
                req=stop(tables[i][1],users)	
            else:
                req=start(tables[i][1],sar['binance'],sar['bitfinex'],sar['bittrex'],sar['kucoin'],sar['okex'],tables[i][6],tables[i][5],tables[i][3],tables[i][7],tables[i][9],users)
                if req=='No':
                    cursor.execute("UPDATE strategies SET status='0' WHERE user_uid=%s"),(tables[i][1])	
    print(now)
    print(len(was),len(now))					
    if len(now)>len(was):
        for i in range(len(was),len(now)):
            sar=json.loads(tables[i][4])
            if now[i]=='0':
                req=stop(tables[i][1],users)	
            else:
                req=start(tables[i][1],sar['binance'],sar['bitfinex'],sar['bittrex'],sar['kucoin'],sar['okex'],tables[i][6],tables[i][5],tables[i][3],tables[i][7],tables[i][9],users)
                if req=='No':
                    cursor.execute("UPDATE strategies SET status='0' WHERE user_uid=%s"),(tables[i][1])			

		
