#************************************************************************************************
#  Aplicación:    Bingo Virtual MySQL                                                           # 
#  Desarrollador: Junior Sulbaran                                                               #
#  Empresa:       ADFSoft                                                                       #
#  Año:           2024                                                                          #
#************************************************************************************************ 

import mysql.connector
from dotenv import load_dotenv
import os

#variables globales .env
# Parámetros de conexión a la base de datos
host = '10.0.0.63' #os.getenv('IP')     #'10.132.201.185'
user ='root' #os.getenv('USER')     #'admin'
password = ''#os.getenv('PASSWORD') #'admin'
database = 'bingodb' #os.getenv('DATABASE') #'ingesta_bd'

# Conexión a MySql
def conectar_base_datos():
  intentos = 0
  max_intentos = 3
  while intentos < max_intentos:
    try:
        # Intentar establecer la conexión
        mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
        return mydb 
    except mysql.connector.Error as error: 
      # Si la conexión falla, imprimir un mensaje de error
      print(f'Error al conectar a la base de datos: {error}')
      # Incrementar el número de intentos
      intentos += 1
      #Esperar un tiempo antes de intentar nuevamente
      
    if intentos == max_intentos:
      # Si se supera el número máximo de intentos, mostrar un mensaje de error
      print('No se pudo establecer la conexión a la base de datos después de varios intentos.')
      # Llamar a la función para intentar conectar a la base de datos
      conectar_base_datos()
