import sqlite3
import time
conn = sqlite3.connect('BD.db')	
cursor = conn.cursor()
tag='%#hello%'
date=int(time.time())
results=[]
stop=[86400,259200,604800,2592000]
datel=0
cursor.execute("SELECT text FROM mess WHERE text LIKE :tag",{"tag":tag})
results1 = cursor.fetchall()
cursor.execute("SELECT date FROM mess WHERE text LIKE :tag",{"tag":tag})
results2 = cursor.fetchall()
cursor.execute("SELECT user FROM mess WHERE text LIKE :tag",{"tag":tag})
results3 = cursor.fetchall()
cursor.execute("SELECT gid FROM mess WHERE text LIKE :tag",{"tag":tag})
results4 = cursor.fetchall()
for i in range(0,len(results1)):
    print(results4[i])
    if (date-int(str(results2[i])[1:-2]))<stop[datel]:
        print(str(results1[i])[2:-3]+' @'+str(results3[i])[2:-3])
conn.close() 
a=input()