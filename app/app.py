from flask import Flask,request,redirect,url_for
from flask import render_template,session
import pymysql
from datetime import datetime
from urllib.parse import urlparse
import secrets
import json
import bcrypt

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(20)


#Funciones Basicas de configuracion
user = { 'email':'','password':'','nombre':'','apellido':'','cargo':'','area':'','empresa':'','rol':''}
CONF = {'ID':'', 'ID_ESTACION': '','ESTACION': '', 'ID_TANQUE':'','TANQUE':'', 'PRODUCTO':'', 'DENSIDAD':'', 'TAG_SENSOR':'','DESCRIPCION':'','UM':'', 'RANGO_MIN':'', 'RANGO_MAX':'','TIPO':'','DIRECCION':'','MASCARA':'','PUERTO':'','ID_COMM':'','SERIAL':'','LINEAR':'','ENABLE':'' }
DATA = {'ID':'', 'FECHA_HORA': '','TAG_SENSOR': '', 'MEDIDA':'', 'UM':'','VELOCIDAD':'','LATITUD':'', 'LONGITUD':'' }
CONX = { 'NOMBRE':'','DIRECCION':'','ENABLE':''}


#Inicializa las tablas necesarias dentro del dispositivo

def init_db():    
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query="SHOW TABLES FROM MAIN_SENSOR"
    cursor.execute(Query)
    lon=cursor.rowcount
    if lon<=0:
        password = "12345"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        Query= "CREATE TABLE CONF ( `ID` INT PRIMARY KEY AUTO_INCREMENT, `ID_ESTACION` TEXT NOT NULL ,`ESTACION` TEXT NOT NULL,`ID_TANQUE` TEXT NOT NULL,`TANQUE` TEXT NOT NULL,`PRODUCTO` TEXT NOT NULL,`DENSIDAD` TEXT NOT NULL,`TAG_SENSOR` TEXT NOT NULL UNIQUE,`DESCRIPCION` TEXT NOT NULL,`UM` TEXT NOT NULL, `RANGO_MIN` FLOAT NOT NULL, `RANGO_MAX` FLOAT NOT NULL, `TIPO` TEXT NOT NULL,`DIRECCION` TEXT NOT NULL, `MASCARA` TEXT NOT NULL, `PUERTO` TEXT NOT NULL,`ID_COMM` TEXT NOT NULL,`SERIAL` TEXT NOT NULL,`LINEAR` TEXT NOT NULL,`ENABLE` TEXT NOT NULL)"
        cursor.execute(Query)
        Query= "CREATE TABLE DATA ( `ID` INT PRIMARY KEY AUTO_INCREMENT , `FECHA_HORA` DATETIME NOT NULL,`TAG_SENSOR` TEXT NOT NULL,`UM` TEXT NOT NULL,`MEDIDA` FLOAT NOT NULL, `VELOCIDAD` FLOAT NOT NULL, `LATITUD` FLOAT NOT NULL,`LONGITUD` FLOAT NOT NULL)"
        cursor.execute(Query)
        Query="CREATE TABLE USER (NOMBRE TEXT NOT NULL, APELLIDO TEXT NOT NULL,EMAIL TEXT NOT NULL UNIQUE, PASSWORD TEXT NOT NULL, CARGO TEXT, AREA TEXT, EMPRESA TEXT, ROL TEXT NOT NULL);"
        cursor.execute(Query)
        Query="CREATE TABLE CONX (NOMBRE TEXT NOT NULL UNIQUE, DIRECCION TEXT NOT NULL, ENABLE TEXT NOT NULL);"
        cursor.execute(Query)
        Query="INSERT INTO USER (NOMBRE,APELLIDO,EMAIL,PASSWORD,ROL) VALUES ('MIGUEL','AGUIRRE','miguelaguirreleon@gmail.com','%s','Administrador');" % hashed.decode('UTF-8')
        cursor.execute(Query)
        connection.commit()
    cursor.close()
    connection.close()  

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






@app.route('/')
@app.route('/index')
def index():
    init_db()
    return render_template('index.html')

@app.route('/dashboard', methods=["GET","POST"])
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        if request.method=="POST":
            user={}
            user['email']=request.form.get("email")
            user['password']=request.form.get("password")
            if val_user(user):
                session['username']=user['email']
                user = {}
                return render_template('dashboard.html')
            else:
                return redirect(url_for('index'))
        else:
                return redirect(url_for('index'))

@app.route('/saveconf', methods=["GET","POST"])
def saveconf():
    if request.method=="POST":
        CONF['ID_ESTACION']=request.form.get("ID_ESTACION")
        CONF['ESTACION']=request.form.get("ESTACION")
        CONF['ID_TANQUE']=request.form.get("ID_TANQUE")
        CONF['TANQUE']=request.form.get("TANQUE")
        CONF['PRODUCTO']=request.form.get("PRODUCTO")
        CONF['DENSIDAD']=request.form.get("DENSIDAD")
        CONF['TAG_SENSOR']=request.form.get("TAG_SENSOR")
        CONF['DESCRIPCION']=request.form.get("DESCRIPCION")
        CONF['UM']=request.form.get("UM")
        CONF['TIPO']=request.form.get("TIPO")
        CONF['RANGO_MIN']=request.form.get("RANGO_MIN")
        CONF['RANGO_MAX']=request.form.get("RANGO_MAX")
        CONF['DIRECCION']=request.form.get("DIRECCION")
        CONF['MASCARA']=request.form.get("MASCARA")
        CONF['PUERTO']=request.form.get("PUERTO")
        CONF['ID_COMM']=request.form.get("ID_COMM")
        CONF['SERIAL']=request.form.get("SERIAL")
        CONF['LINEAR']=request.form.get("LINEAR")       
        CONF['ENABLE']=request.form.get("ENABLE")
        if check_conf(CONF):
            return update_conf(CONF)
        else:
            return save_conf(CONF)
    else:
        message = {
            'status': 404,
            'message': 'FAIL',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/getconf', methods=["GET","POST"])
def getconf():
    if request.method=="POST":
        CONF['TAG_SENSOR']=request.form.get("TAG_SENSOR")
        return get_conf(CONF)
    else:
        message = {
            'status': 404,
            'message': 'FAIL',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/usuarios')
def usuarios():
    if 'username' in session:
        return render_template('usuarios.html')
    else:
        return redirect(url_for('index'))

@app.route('/configuracion')
def configuracion():
    if 'username' in session:
        return render_template('configuracion.html')
    else:
        return redirect(url_for('index'))

@app.route('/nodos')
def nodos():
    if 'username' in session:
        return render_template('nodos.html')
    else:
        return redirect(url_for('index'))

@app.route('/getuser', methods=["GET","POST"])
def getuser():
    if 'username' in session:
        if request.method=="POST":
            user['email']=request.form.get("email")
            return get_user(user)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 0
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/saveuser', methods=["GET","POST"])
def saveuser():
    if 'username' in session:
        if request.method=="POST":
            user['nombre']=request.form.get("nombre")
            user['apellido']=request.form.get("apellido")
            user['cargo']=request.form.get("cargo")
            user['rol']=request.form.get("rol")
            user['area']=request.form.get("area")
            user['empresa']=request.form.get("empresa")
            user['email']=request.form.get("email")
            user['password']=request.form.get("password")
            user['npassword']=request.form.get("npassword")
            if check_user(user):
                return update_user(user)
            else:
                return save_user(user)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 'Actualizacion Fallida'
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)


@app.route('/getnodo', methods=["GET","POST"])
def getnodo():
    if 'username' in session:
        if request.method=="POST":
            CONX['NOMBRE']=request.form.get("NOMBRE")
            return get_nodo(CONX)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 0
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/savenodo', methods=["GET","POST"])
def savenodo():
    if 'username' in session:
        if request.method=="POST":
            CONX['NOMBRE']=request.form.get("NOMBRE")
            CONX['DIRECCION']=request.form.get("DIRECCION")
            CONX['ENABLE']=request.form.get("ENABLE")
            if check_nodo(CONX):
                return update_nodo(CONX)
            else:
                return save_nodo(CONX)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 'Actualizacion Fallida'
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')
