import pymysql
from urllib.parse import urlparse
import json


#Administracion de Configuracion
def check_conf(CONF):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM `CONF` WHERE `TAG_SENSOR`= %s' 
    cursor.execute(Query,(CONF['TAG_SENSOR']))
    e=cursor.fetchone()
    lon=cursor.rowcount
    if lon>0:
        return True
    else:
        return False

def save_conf(CONF):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='INSERT INTO CONF (`ID_ESTACION`,`ESTACION`,`ID_TANQUE` ,`TANQUE` ,`PRODUCTO` ,`DENSIDAD` ,`TAG_SENSOR` ,`DESCRIPCION` ,`UM` , `RANGO_MIN` , `RANGO_MAX`, `TIPO` ,`DIRECCION`, `MASCARA`, `PUERTO`,`ID_COMM`,`SERIAL`,`LINEAR`,`ENABLE`) VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(Query,(CONF['ID_ESTACION'],CONF['ESTACION'],CONF['ID_TANQUE'] ,CONF['TANQUE'] ,CONF['PRODUCTO'] ,CONF['DENSIDAD'] ,CONF['TAG_SENSOR'] ,CONF['DESCRIPCION'] ,CONF['UM'] ,CONF['RANGO_MIN'] , CONF['RANGO_MAX'], CONF['TIPO'] ,CONF['DIRECCION'], CONF['MASCARA'], CONF['PUERTO'],CONF['ID_COMM'],CONF['SERIAL'],CONF['LINEAR'],CONF['ENABLE']))
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

def update_conf(CONF):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='UPDATE CONF SET `ID_ESTACION`= %s ,`ESTACION`= %s,`ID_TANQUE`= %s ,`TANQUE`= %s ,`PRODUCTO`= %s ,`DENSIDAD`= %s ,`TAG_SENSOR`= %s ,`DESCRIPCION`=%s ,`UM`=%s , `RANGO_MIN`=%s , `RANGO_MAX`=%s, `TIPO`=%s ,`DIRECCION`=%s, `MASCARA`=%s, `PUERTO`=%s,`ID_COMM`=%s,`SERIAL`=%s,`LINEAR`=%s,`ENABLE`=%s WHERE TAG_SENSOR = %s'
    cursor.execute(Query,(CONF['ID_ESTACION'],CONF['ESTACION'],CONF['ID_TANQUE'],CONF['TANQUE'],CONF['PRODUCTO'],CONF['DENSIDAD'],CONF['TAG_SENSOR'],CONF['DESCRIPCION'],CONF['UM'],CONF['RANGO_MIN'],CONF['RANGO_MAX'],CONF['TIPO'],CONF['DIRECCION'],CONF['MASCARA'],CONF['PUERTO'],CONF['ID_COMM'],CONF['SERIAL'],CONF['LINEAR'],CONF['ENABLE'],CONF['TAG_SENSOR']))
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

def get_conf(CONF):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query="SELECT * FROM `CONF` WHERE TAG_SENSOR= %s" 
    cursor.execute(Query,CONF['TAG_SENSOR'])
    data=cursor.fetchone()
    lon=cursor.rowcount
    cursor.close()
    connection.close()
    CONF = {'ID':'', 'ID_ESTACION': '','ESTACION': '', 'ID_TANQUE':'','TANQUE':'', 'PRODUCTO':'', 'DENSIDAD':'', 'TAG_SENSOR':'','DESCRIPCION':'','UM':'', 'RANGO_MIN':'', 'RANGO_MAX':'','TIPO':'','DIRECCION':'','MASCARA':'','PUERTO':'','ID_COMM':'','SERIAL':'','LINEAR':'','ENABLE':'' }
    if lon>0:   
        CONF['ID_ESTACION']=data[1]
        CONF['ESTACION']=data[2]
        CONF['ID_TANQUE']=data[3]
        CONF['TANQUE']=data[4]
        CONF['PRODUCTO']=data[5]
        CONF['DENSIDAD']=data[6]
        CONF['TAG_SENSOR']=data[7]
        CONF['DESCRIPCION']=data[8]
        CONF['UM']=data[9]
        CONF['RANGO_MIN']=data[10]
        CONF['RANGO_MAX']=data[11]
        CONF['TIPO']=data[12]
        CONF['DIRECCION']=data[13]
        CONF['MASCARA']=data[14]
        CONF['PUERTO']=data[15]
        CONF['ID_COMM']=data[16]
        CONF['SERIAL']=data[17]
        CONF['LINEAR']=data[18]
    message = {
        'status': 200,
        'message': 'OK',
        'data': CONF
    }
    resp =  json.dumps(message, indent=4)
    return resp


