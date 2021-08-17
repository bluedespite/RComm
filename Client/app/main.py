import pymysql
import logging
from datetime import datetime
from pymodbus.client.sync import ModbusTcpClient
import time
import serial
import serial.tools.list_ports
import threading



CONF = {'ID':'', 'ID_ESTACION': '','ESTACION': '', 'ID_TANQUE':'','TANQUE':'', 'PRODUCTO':'', 'DENSIDAD':'', 'TAG_SENSOR':'','DESCRIPCION':'','UM':'', 'RANGO_MIN':'', 'RANGO_MAX':'','TIPO':'','DIRECCION':'','MASCARA':'','PUERTO':'','ID_COMM':'','SERIAL':'','LINEAR':'','ENABLE':'' }
DATA = {'ID':'', 'FECHA_HORA': '','TAG_SENSOR': '', 'MEDIDA':'', 'UM':'','VELOCIDAD':'','LATITUD':'', 'LONGITUD':'', 'SALE':'', 'DELIVERY':'' }
ARDUINO={'Latitude': 0, 'Longitude': 0, 'Velocity': 0, '0': 0, '1':0, '2':0,'3':0, '4':0}


def init_logger():
    FORMAT = ('%(asctime)s - %(threadName)s %(levelname)s %(module)s %(lineno)s %(message)s')
    logging.basicConfig(filename='Roraima_Log.txt', filemode='w',format=FORMAT)
    log=logging.getLogger()
    log.setLevel(logging.DEBUG)

def init_arduino():   
    arduino_ports=[]
    for p in serial.tools.list_ports.comports():
        if 'Arduino' in p.manufacturer:
            arduino_ports = p.device
            logging.info("Info Puerto Serie Arduino:"+str(p.device))
            return arduino_ports,True
    return arduino_ports,False

def Arduino_Comm():
    arduino_port,OK = init_arduino()
    arduino = serial.Serial(arduino_port,9600, timeout=50)
    time.sleep(10)
    if OK:
        comando = 'GO!'+'\n'
        a=arduino.write(comando.encode())
        lectura = arduino.readline() 
        txt=str(lectura)
        txt=txt[2:-5]
        if txt.find('Latitude')<0  or txt.find('Longitude')<0:
            logging.info("Error de lectura en cadena Serial")
        else:
            SerialA=txt.split("|")
            for S in SerialA:
                CLAVE=S.split("=")[0]
                VALOR=S.split("=")[1]
                if VALOR=="INVALID DATETIME":
                    VALOR=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if VALOR=="INVALID SPEED":
                    VALOR="0"
                if VALOR=="INVALID LATITUDE":
                    VALOR=LAST_VALID_LAT
                if VALOR=="INVALID LONGITUDE":
                    VALOR=LAST_VALID_LON
                if CLAVE=="Latitude":
                    LAST_VALID_LAT=VALOR
                if CLAVE=="Longitude":
                    LAST_VALID_LON=VALOR
                ARDUINO[CLAVE]=VALOR
    else:
        logging.error("No se puede contectar a Tarjeta ARDUINO")    
    return Arduino

init_logger()
data=Arduino_Comm()
print(data)