import pymysql
from datetime import datetime
from urllib.parse import urlparse
import bcrypt
import json

#Login de usuarios
def val_user(user):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor= connection.cursor()
    Query="SELECT PASSWORD FROM `USER` WHERE email = %s"
    cursor.execute(Query,(user['email']))
    e=cursor.fetchone()
    cursor.close()
    connection.close()    
    try:
        hashed=e[0].encode('UTF-8')
        return bcrypt.checkpw(user['password'].encode('UTF-8'), hashed)
    except:
        return False
#Administracion de usuarios
def check_user(user):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM `USER` WHERE email=%s'
    cursor.execute(Query,(user['email']))
    lon=cursor.rowcount
    if lon>0:
        return True
    else:
        return False

def save_user(user):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    password = user['password'].encode('UTF-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    user['hashed'] = hashed.decode('UTF-8')
    Query='INSERT INTO USER (NOMBRE,APELLIDO,EMAIL,PASSWORD,CARGO, AREA, ROL,EMPRESA) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(Query,(user['nombre'],user['apellido'],user['email'],user['hashed'],user['cargo'],user['area'],user['rol'],user['empresa']))
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

def update_user(user):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    password = user['npassword'].encode('UTF-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    user['hashed'] = hashed.decode('UTF-8')
    Query='UPDATE USER SET NOMBRE = %s, APELLIDO = %s , CARGO = %s, PASSWORD = %s, AREA = %s, EMPRESA = %s, ROL = %s WHERE EMAIL = %s'
    cursor.execute(Query,(user['nombre'],user['apellido'],user['cargo'],user['hashed'],user['area'],user['empresa'],user['rol'],user['email']))
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

def get_user(user):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM USER WHERE email = %s '
    cursor.execute(Query,(user['email']))
    data=cursor.fetchone()
    lon=cursor.rowcount
    cursor.close()
    connection.close()
    user = { 'email':'','password':'','nombre':'','apellido':'','cargo':'','area':'','empresa':'','rol':''}
    if lon>0:
        user['nombre']=data[0]
        user['apellido']=data[1]
        user['email']=data[2]
        user['cargo']=data[4]
        user['area']=data[5]
        user['empresa']=data[6]
        user['rol']=data[7]
    message = {
        'status': 200,
        'message': 'OK',
        'data': user
    }
    resp =  json.dumps(message, indent=4)
    return resp
