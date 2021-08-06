import matplotlib.pyplot as plt
from datetime import datetime
import random
import numpy as np
import pymysql
from urllib.parse import urlparse
prct=0.005 #0.5% de cambios
testdb='mysql://admin:12345@localhost/MAIN_SENSOR'
def sin_wave():
    dbc = urlparse(testdb)
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    TOT_D=0
    TOT_S=0
    D=[]
    y=[]
    x=[]
    f=1/100
    VANT=0
    DATA = {'ID':'', 'FECHA_HORA': '','TAG_SENSOR': 'LVL01', 'MEDIDA':'', 'UM':'GAL','VELOCIDAD':'','LATITUD':'', 'LONGITUD':'', 'SALE':'', 'DELIVERY':'' }
    for x1 in range(0,1000):
        DATA['MEDIDA'] = 1200*np.sin(x1*f)+random.random()/1000
        if DATA['MEDIDA']<0:
            DATA['MEDIDA']=0
        if DATA['MEDIDA']>1000:
            DATA['MEDIDA']=1000
        DATA['SALE']=0
        DATA['DELIVERY']=0
        if DATA['MEDIDA']-VANT>0.2:
            DATA['DELIVERY']=DATA['MEDIDA']-VANT
            TOT_D+=DATA['DELIVERY']
        if VANT-DATA['MEDIDA']>0.2:
            DATA['SALE']=VANT-DATA['MEDIDA']
            TOT_S+=DATA['SALE']
        VANT=DATA['MEDIDA']
        y.append(DATA['MEDIDA'])
        x.append(x1)
        DATA['LATITUD']= -12.063190+random.random()/1000
        DATA['LONGITUD']= -77.112600+random.random()/1000
        DATA['VELOCIDAD']= 100*random.random()
        DATA['FECHA_HORA']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        D.append(DATA)
        Query='INSERT INTO DATA (FECHA_HORA, TAG_SENSOR,MEDIDA,UM,VELOCIDAD,LATITUD,LONGITUD, SALE,DELIVERY) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(Query,(DATA['FECHA_HORA'],DATA['TAG_SENSOR'],DATA['MEDIDA'],DATA['UM'], DATA['VELOCIDAD'],DATA['LATITUD'],DATA['LONGITUD'],DATA['SALE'],DATA['DELIVERY']))
    connection.commit()
    cursor.close()
    connection.close()
    plt.plot(x,y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Señal de prueba')
    plt.show()
    print(TOT_D)
    print(TOT_S)
    return D

DATA=sin_wave()

