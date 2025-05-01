#************************************************************************************************
#  Aplicación:    Bingo Virtual MySQL                                                           # 
#  Desarrollador: Junior Sulbaran                                                               #
#  Empresa:       ADFSoft                                                                       #
#  Año:           2024                                                                          #
#************************************************************************************************ 

import mysql.connector
from dotenv import load_dotenv
import os
import time

# Variables globales .env
host = '10.0.0.63'  # os.getenv('IP')
user = 'root'  # os.getenv('USER')
password = ''  # os.getenv('PASSWORD')
database = 'bingodb'  # os.getenv('DATABASE')

def verificar_conexion(mydb):
    """Verifica si la conexión está activa y válida"""
    try:
        if mydb and mydb.is_connected():
            mydb.ping(reconnect=True, attempts=3, delay=1)
            return True
    except mysql.connector.Error:
        pass
    return False

# Conexión a MySql mejorada
def conectar_base_datos():
    intentos = 0
    max_intentos = 3
    tiempo_espera = 1  # segundos entre intentos
    ultimo_error = None
    
    while intentos < max_intentos:
        try:
            # Intentar establecer la conexión
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                connect_timeout=5
            )
            
            # Verificar conexión exitosa
            if verificar_conexion(mydb):
                return mydb
            
        except mysql.connector.Error as error:
            ultimo_error = error
            print(f'Error al conectar a la base de datos (intento {intentos + 1}): {error}')
            intentos += 1
            if intentos < max_intentos:
                time.sleep(tiempo_espera)  # Espera antes de reintentar
    
    # Si llegamos aquí, todos los intentos fallaron
    error_msg = f'No se pudo establecer la conexión después de {max_intentos} intentos. Último error: {ultimo_error}'
    print(error_msg)
    raise Exception(error_msg)  # Lanza excepción en lugar de retornar None