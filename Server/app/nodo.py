import pymysql
from urllib.parse import urlparse
import json

#Administracion de conexiones de nodos
def check_nodo(CONX):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM `CONX` WHERE `NOMBRE`= %s' 
    cursor.execute(Query,(CONX['NOMBRE']))
    e=cursor.fetchone()
    lon=cursor.rowcount
    if lon>0:
        return True
    else:
        return False

def save_nodo(CONX):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='INSERT INTO CONX (`NOMBRE`,`DIRECCION`,`ENABLE`) VALUES ( %s,%s,%s)'
    cursor.execute(Query,(CONX['NOMBRE'],CONX['DIRECCION'],CONX['ENABLE']))
    connection.commit()
    cursor.close()
    connection.close()
    message = {
            'status': 200,
            'message': 'OK',
            'data': 'Se insertó registro'
        }
    resp =  json.dumps(message, indent=4)
    return resp

def update_nodo(CONX):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='UPDATE CONX SET `DIRECCION`= %s ,`ENABLE`= %s WHERE NOMBRE = %s'
    cursor.execute(Query,(CONX['DIRECCION'],CONX['ENABLE'],CONX['NOMBRE']))
    connection.commit()
    cursor.close()
    connection.close()
    message = {
            'status': 200,
            'message': 'OK',
            'data': 'Se actualizó Registro'
        }
    resp =  json.dumps(message, indent=4)
    return resp

def get_nodo(CONX):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query="SELECT * FROM `CONX` WHERE NOMBRE= %s" 
    cursor.execute(Query,CONX['NOMBRE'])
    data=cursor.fetchone()
    lon=cursor.rowcount
    cursor.close()
    connection.close()
    CONF = {'NOMBRE':'', 'DIRECCION': '','ENABLE': '' }
    if lon>0:   
        CONF['NOMBRE']=data[0]
        CONF['DIRECCION']=data[1]
        CONF['ENABLE']=data[2]
    message = {
        'status': 200,
        'message': 'OK',
        'data': CONF
    }
    resp =  json.dumps(message, indent=4)
    return resp
