import pymysql
from urllib.parse import urlparse
import json


def dateconvert(date):
    datos=[]
    for i in range(len(date)):
        datos.append(date[i][0].strftime('%Y-%m-%d %H:%M:%S'))
    return datos

#Datos para graficas entre fecha_inicio y fecha_fin
def Queryalldatos(fecha_inicio,fecha_fin):
    print(fecha_inicio)
    print(fecha_fin)
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query="SELECT TAG_SENSOR FROM `DATA` WHERE FECHA_HORA>%s AND FECHA_HORA<%s GROUP BY TAG_SENSOR"
    cursor.execute(Query,(fecha_inicio,fecha_fin))
    tags=cursor.fetchall()
    Query="SELECT FECHA_HORA FROM `DATA` WHERE FECHA_HORA>%s AND FECHA_HORA<%s "
    cursor.execute(Query,(fecha_inicio,fecha_fin))
    labels=dateconvert(cursor.fetchall())
    data=[]
    for tag in tags:
        Query="SELECT FECHA_HORA FROM `DATA` WHERE TAG_SENSOR = %s AND FECHA_HORA>%s AND FECHA_HORA<%s  "
        cursor.execute(Query, (tag,fecha_inicio,fecha_fin))
        x=dateconvert(cursor.fetchall())
        Query="SELECT MEDIDA FROM `DATA` WHERE TAG_SENSOR = %s AND FECHA_HORA>%s AND FECHA_HORA<%s"
        cursor.execute(Query, (tag,fecha_inicio,fecha_fin))
        y=[T[0] for T in cursor.fetchall()]
        Query="SELECT SUM(SALE) FROM `DATA` WHERE TAG_SENSOR = %s AND FECHA_HORA>%s AND FECHA_HORA<%s"
        cursor.execute(Query, (tag,fecha_inicio,fecha_fin))
        q1=cursor.fetchone()
        Query="SELECT SUM(DELIVERY) FROM `DATA` WHERE TAG_SENSOR = %s AND FECHA_HORA>%s AND FECHA_HORA<%s"
        cursor.execute(Query, (tag,fecha_inicio,fecha_fin))
        q2=cursor.fetchone()
        Query="SELECT UM FROM `DATA` WHERE TAG_SENSOR = %s AND FECHA_HORA>%s AND FECHA_HORA<%s ORDER BY ID DESC LIMIT 1"
        cursor.execute(Query, (tag,fecha_inicio,fecha_fin))
        q3=cursor.fetchone()
        Query="SELECT LATITUD,LONGITUD FROM `DATA` WHERE TAG_SENSOR = %s AND FECHA_HORA>%s AND FECHA_HORA<%s ORDER BY ID DESC LIMIT 1"
        cursor.execute(Query, (tag,fecha_inicio,fecha_fin))
        geo=cursor.fetchall()
        q00=[]
        for i in range(len(x)):
            q00.append({
                'x':x[i],
                'y':y[i],
           })
        data.append({
            'DATA':q00,
            'TAG_SENSOR': tag,
            'UM': q3
        })
    cursor.close
    connection.close
    return labels,data



def get_chartdata(fecha_inicio,fecha_fin):
    import random
    labels,datos=Queryalldatos(fecha_inicio.replace('T',' '),fecha_fin.replace('T',' '))
    datasets=[]
    for i in range(len(datos)):
        color=str(255*random.random())+','+str(255*random.random())+','+str(255*random.random())
        datasets.append({
            'label':datos[i]['TAG_SENSOR'],
            'data': datos[i]['DATA'],
            'lineTension': '0',
            'backgroundColor': 'rgba('+color+',0.2)',
            'borderColor': 'rgba('+color+',1)'})
    chartdata={'labels':labels, 'datasets': datasets}
    message = {
            'status': 200,
            'message': 'OK',
            'data': chartdata
        }
    resp =  json.dumps(message, indent=4)
    return resp

def Querybardata(fecha_inicio,fecha_fin):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query="SELECT TAG_SENSOR,SUM(SALE),SUM(DELIVERY) FROM `DATA` WHERE FECHA_HORA>%s AND FECHA_HORA<%s GROUP BY TAG_SENSOR"
    cursor.execute(Query,(fecha_inicio,fecha_fin))
    datos=cursor.fetchall()
    data={
        'labels': [T[0] for T in datos],
        'datasets': [
        {'label': "Sales",
          'backgroundColor': "#3e95cd",
          'data': [T[1] for T in datos]
        }, {
          'label': "Deliveries",
          'backgroundColor': "#8e5ea2",
          'data': [T[2] for T in datos]
        }]}
    return data




def get_bardata(fecha_inicio,fecha_fin):
    datos=Querybardata(fecha_inicio.replace('T',' '),fecha_fin.replace('T',' '))
    message = {
            'status': 200,
            'message': 'OK',
            'data': datos
        }
    resp =  json.dumps(message, indent=4)
    return resp

#Datos para graficas entre fecha_inicio y fecha_fin
def Querygeodatos(fecha_inicio,fecha_fin):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    size=0
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query="SELECT TAG_SENSOR FROM `DATA` WHERE FECHA_HORA>%s AND FECHA_HORA<%s GROUP BY TAG_SENSOR"
    cursor.execute(Query,(fecha_inicio,fecha_fin))
    tags=cursor.fetchall()
    data=[]
    for tag in tags:
        Query="SELECT LATITUD,LONGITUD FROM `DATA` WHERE TAG_SENSOR = %s AND FECHA_HORA>%s AND FECHA_HORA<%s "
        cursor.execute(Query, (tag,fecha_inicio,fecha_fin))
        geo=cursor.fetchall()
        data.append({
            'TAG_SENSOR': tag,
            'GEO':geo
        })
        size+=1
    cursor.close
    connection.close
    return size,data


def get_geomap(fecha_inicio,fecha_fin):
    size,data=Querygeodatos(fecha_inicio,fecha_fin)    
    message = {
            'status': 200,
            'message': 'OK',
            'data':data
        }
    resp =  json.dumps(message, indent=4)
    return resp
