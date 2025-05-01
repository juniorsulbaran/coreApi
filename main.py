#importar librerias
from flask import Flask, jsonify, request,render_template,redirect,url_for,flash,session
# Importando las clases SocketIO y emit del módulo flask_socketio
from flask_socketio import SocketIO, emit
from flask_session import Session
import time
import pandas as pd
from generarCartonBingo import matriz
from consultasdb import *
from dotenv import load_dotenv
import os
from conexiones import conectar_base_datos 
from bolRandom import cantarBola
from letraRandom import cantarLetra
from verificaEmail import enviarCorreoVerificacion, obtener_verificacion_por_email
import threading
import pytz
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

#variables sorteo letra
contadorSorteo = 0
sorteoletra = ''
hora_12h=''
montoDisponible=''
# Definir la zona horaria de Venezuela
tz_venezuela = pytz.timezone('America/Caracas')
# Obtener la hora actual en Venezuela
hora_actual_venezuela = datetime.now(tz_venezuela)
print("La hora actual en Venezuela es:", hora_actual_venezuela.strftime('%d-%m-%Y %H:%M:%S'))
# Definir la zona horaria de Colombia
tz_colombia = pytz.timezone('America/Bogota')
# Obtener la hora actual en Colombia
hora_actual_colombia = datetime.now(tz_colombia)
print("La hora actual en Colombia  es:", hora_actual_colombia.strftime('%d-%m-%Y %H:%M:%S'))

now = hora_actual_venezuela.strftime('%Y-%m-%d %H:%M:%S')
nowDate = hora_actual_venezuela.strftime('%d-%m-%Y')
diaSiguiente = nowDate
print(nowDate)
# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'

# para crear una instancia de Socket.IO en una aplicación Flask
socketio = SocketIO(app)

db = conectar_base_datos()

# Configurar la duración de la sesión (5 minutos)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

@app.before_request
def before_request():
    # Reiniciar el temporizador de la sesión en cada solicitud
    session.permanent = True  # La sesión expirará después de 5 minutos de inactividad
    # Opcional: También puedes modificar manualmente 'session.modified = True' para reiniciar el tiempo

# Escuchando si el servidor esta conectado del lado del servidor
@socketio.on('connect')
def handle_connect():
    emit("¡Bienvenido!")

#Hora del servidor
@socketio.on('hora')
def hora(hora):
    print(hora)
    while True:
        time.sleep(1)
        listarResultadoLetra = resultadoLetra(nowDate)
        emit('resultadoLetraFecha', listarResultadoLetra, broadcast=True)
        sorteo = sorteopendiente()
        sorteoPendiente = sorteo[0][0]
        vendidos = 1
        listCartonesVendidos = buscarTotalCartonesVendidos1(vendidos,sorteoPendiente,nowDate)
        totalVendidos = listCartonesVendidos[0][0]
        emit('boletoventa', totalVendidos, broadcast=True)
        hora_actual_venezuela = datetime.now(tz_venezuela)
        hora_actual = hora_actual_venezuela.strftime('%H:%M:%S') 
        # Supongamos que tienes una hora en formato 24H
        hora_24h = hora_actual
        # Convertir la cadena a un objeto datetime
        hora_objeto = datetime.strptime(hora_24h, "%H:%M:%S")
        # Formatear la hora en formato 12H
        hora_12h = hora_objeto.strftime("%I:%M:%S %p")       
        emit('time', hora_12h, broadcast=True)
        
        
#fecha del servido
@socketio.on('fecha')
def fecha(fecha):
    print(fecha)
    hora_actual_venezuela = datetime.now(tz_venezuela)
    hora_actual = hora_actual_venezuela.strftime('%d/%m/%Y')     
    emit('date', hora_actual, broadcast=True)


# Escuchando si el cliente se desconecta del lado del servidor
@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')  
  
def sorteoLotto(sorteoletra,nowDate):
    print('Iniciado Sorteo Lotto', sorteoletra, nowDate )
    time.sleep(3)
    letra = cantarLetra()
    guardarLetra = guardoLetraGanadora(letra,sorteoletra,nowDate)
    listarResultadoLetra = resultadoLetra(nowDate)
    #Logica para actualizar sorteo disponible ################################
    #sorteoNuevo = 1
    #pote = sorteopendiente()
    #montoPote = pote[0][1]
    #sorteoTaquilla = BuscarSorteo(sorteoNuevo)
    #actualizoSorteo = updateSorteo(horaSorteo,montoPote,sorteoTaquilla[0][0])
    #print('actualizo proximo',actualizoSorteo)
    ##########################################################################
    
    emit('lotto', letra, broadcast=True)
    emit('resultadoLetraFecha', listarResultadoLetra, broadcast=True)
    print(' Lista resultado Letra: ', listarResultadoLetra) 

    
#iniciamos el sorteo
def recibir_mensaje(msg,pote,nowDate):
    print('Sorteo De: ' + msg)
    print('pote: ', pote)
    horaSorteo = msg
    contadorBola = 0
    premioB = []
    premioI = []
    premioN = []
    premioG = []
    premioO = []
    numero = []
    # contadores por letra para saber cuando ya han salido los 5 digitos de cada letra y asi insertar en 
    # la tabla carton premiado para generar  el carton  ganador 
    contB = 0
    contI = 0
    contN = 0
    contG = 0
    contO = 0
    cantidadPosicionB = ''
    cantidadPosicionI = ''
    cantidadPosicionN = ''
    cantidadPosicionG = ''
    cantidadPosicionO = ''
    bolaCantada = ''
    while True:
        print('#')
        time.sleep(5)
        bolaCantada = cantarBola()
        print('soy Bola Cantada ',bolaCantada[0])
        numero = numeroUnico(bolaCantada[0])
        print('soy el numero en la tabla',numero)
        if numero !=[]:
            print('existo en base de dato',numero)
            emit('agr', 'SORTEO', broadcast=True)
        else:
            cont = contador()
            b = cont[0]
            contadorBola = b[0]
            #esta condicion es solo para iniciar el contado ya que en la base de datos
            # todavia no hay numero unico pero ya se inicio el sorteo
            time.sleep(3)
            if contadorBola == 0:
                contadorBola = 1 
            print('Cantidad de Numeros Sorteados',contadorBola,' / ','75')
            #Clasificamos Los numero cantados Para Generar carton Premiado  
            if int(bolaCantada[0]) >= 1 and int(bolaCantada[0]) <= 15:
                guardoNumeroSorteado(int(bolaCantada[0]))
                bola = {
                    "numero":bolaCantada[0]
                }
                if contB <= 5:
                    cantidadPosicionB = len(premioB)
                    if contB == 0 and cantidadPosicionB == 0:
                        contB += 1
                        premioB.append(int(bolaCantada[0]))
                            
                    if contB == 1 and cantidadPosicionB == 1:
                        contB += 1
                        premioB.append(int(bolaCantada[0]))
                            
                    if contB == 2 and cantidadPosicionB == 2:
                        contB += 1
                        premioB.append(int(bolaCantada[0]))
                            
                    if contB == 3 and cantidadPosicionB == 3:
                        contB += 1
                        premioB.append(int(bolaCantada[0]))
                            
                    if contB == 4 and cantidadPosicionB == 4:
                        contB += 1
                        premioB.append(int(bolaCantada[0]))
                          
                    emit('message', bola, broadcast=True) 
                    
            if int(bolaCantada[0]) >= 16 and int(bolaCantada[0]) <= 30:
                guardoNumeroSorteado(int(bolaCantada[0]))
                bola = {
                    "numero":bolaCantada[0]
                }
                cantidadPosicionI = len(premioI)
                if contI <= 5:
                    if contI == 0 and cantidadPosicionI == 0:
                        contI += 1
                        premioI.append(int(bolaCantada[0]))
                            
                    if contI == 1 and cantidadPosicionI == 1:
                        contI += 1
                        premioI.append(int(bolaCantada[0]))
                            
                    if contI == 2 and cantidadPosicionI == 2:
                        contI += 1
                        premioI.append(int(bolaCantada[0]))
                            
                    if contI == 3 and cantidadPosicionI == 3:
                        contI += 1
                        premioI.append(int(bolaCantada[0]))
                        
                    if contI == 4 and cantidadPosicionI == 4:
                        contI += 1
                        premioI.append(int(bolaCantada[0]))
                        print('Matriz I',premioI)
                        
                    emit('message', bola, broadcast=True) 
                
            if int(bolaCantada[0]) >= 31 and int(bolaCantada[0]) <= 45:
                guardoNumeroSorteado(int(bolaCantada[0]))
                bola = {
                    "numero":bolaCantada[0]
                }
                cantidadPosicionN = len(premioN)
                if contN <= 5:
                    if contN == 0 and cantidadPosicionN == 0:
                        contN+= 1
                        premioN.append(int(bolaCantada[0]))
                            
                    if contN == 1 and cantidadPosicionN == 1:
                        contN+= 1
                        premioN.append(int(bolaCantada[0]))
                        
                    if contN == 2 and cantidadPosicionN == 2:
                        contN+= 1
                        premioN.append(int(bolaCantada[0]))
                            
                    if contN == 3 and cantidadPosicionN == 3:
                        contN+= 1
                        premioN.append(int(bolaCantada[0]))
                            
                    if contN == 4 and cantidadPosicionN == 4:
                        contN+= 1
                        premioN.append(int(bolaCantada[0]))    
                            
                    emit('message', bola, broadcast=True) 
                
            if int(bolaCantada[0]) >= 46 and int(bolaCantada[0]) <= 60:
                guardoNumeroSorteado(int(bolaCantada[0]))
                bola = {
                    "numero":bolaCantada[0]
                }
                cantidadPosicionG = len(premioG)
                if contG <= 5:
                    if contG == 0 and cantidadPosicionG == 0:
                        contG += 1
                        premioG.append(int(bolaCantada[0]))
                            
                    if contG == 1 and cantidadPosicionG == 1:
                        contG += 1
                        premioG.append(int(bolaCantada[0]))
                            
                    if contG == 2 and cantidadPosicionG == 2:
                        contG += 1
                        premioG.append(int(bolaCantada[0]))
                            
                    if contG == 3 and cantidadPosicionG == 3:
                        contG += 1
                        premioG.append(int(bolaCantada[0]))
                            
                    if contG == 4 and cantidadPosicionG == 4:
                        contG += 1
                        premioG.append(int(bolaCantada[0]))
                           

                    emit('message', bola, broadcast=True) 
                    
            if int(bolaCantada[0]) >= 61 and int(bolaCantada[0]) <= 75:
                guardoNumeroSorteado(int(bolaCantada[0]))
                bola = {
                    "numero":bolaCantada[0]
                }
                cantidadPosicionO = len(premioO)
                if contO <= 5:
                    if contO == 0 and cantidadPosicionO == 0:
                        contO += 1
                        premioO.append(int(bolaCantada[0]))
                            
                    if contO == 1 and cantidadPosicionO == 1:
                        contO+= 1
                        premioO.append(int(bolaCantada[0]))
                            
                    if contO == 2 and cantidadPosicionO == 2:
                        contO+= 1
                        premioO.append(int(bolaCantada[0]))
                            
                    if contO == 3 and cantidadPosicionO == 3:
                        contO+= 1
                        premioO.append(int(bolaCantada[0]))
                            
                    if contO == 4 and cantidadPosicionO == 4: 
                        contO+= 1
                        premioO.append(int(bolaCantada[0]))
                                                      
                    emit('message', bola, broadcast=True) 
        print('Hora Sorteo: ', horaSorteo)   
        print('Matriz Completa B:', premioB) 
        print('Matriz Completa I:', premioI) 
        print('Matriz Completa N:', premioN)  
        print('Matriz Completa G:', premioG) 
        print('Matriz Completa O:', premioO)
        matrizB = len(premioB)
        matrizI = len(premioI)
        matrizN = len(premioN)
        matrizG = len(premioG)
        matrizO = len(premioO) 
        if matrizB == 5 and matrizI == 5 and matrizN == 5 and matrizG == 5 and matrizO == 5:
            #Grito de Bingo
            emit('bingo', 'BINGO', broadcast=True)
            numeroUnicoEliminado = borrarTablaNumeroUnico()
            #Guardamos el clon del premio
            cartonPremio = cartonPremiado(horaSorteo,nowDate,premioB,premioI,premioN,premioG,premioO)
            
            if horaSorteo == '09:30:00':
                sorteoNuevo = 2
                sorteoTaquilla = BuscarSorteo(sorteoNuevo)
                print('sorteo taquilla',sorteoTaquilla[0][0])
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(horaSorteo,montoPote,sorteoTaquilla[0][0])
                print('actualizo proximo',actualizoSorteo)
                time.sleep(10) #prueba enviar inicio sorteo
                emit('sorteo', sorteoTaquilla, broadcast=True)
                emit('agr', 'SORTEO', broadcast=True)
                emit('pote',montoPote, broadcast=True)
                horaSorteo = sorteoTaquilla
                emit('limpiarSala','sala', broadcast=True)
            
            if horaSorteo == '10:30:00':
                sorteoNuevo = 3
                sorteoTaquilla = BuscarSorteo(sorteoNuevo)
                print('sorteo taquilla',sorteoTaquilla[0][0])
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(horaSorteo,montoPote,sorteoTaquilla[0][0])
                print('actualizo proximo',actualizoSorteo)
                time.sleep(10) #prueba enviar inicio sorteo
                emit('sorteo', sorteoTaquilla, broadcast=True)
                emit('agr', 'SORTEO', broadcast=True)
                emit('pote',montoPote, broadcast=True)
                horaSorteo = sorteoTaquilla
                emit('limpiarSala','sala', broadcast=True)
                
            if horaSorteo == '11:30:00':
                sorteoNuevo = 4
                sorteoTaquilla = BuscarSorteo(sorteoNuevo)
                print('sorteo taquilla',sorteoTaquilla[0][0])
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(horaSorteo,montoPote,sorteoTaquilla[0][0])
                print('actualizo proximo',actualizoSorteo)
                time.sleep(10) #prueba enviar inicio sorteo
                emit('sorteo', sorteoTaquilla, broadcast=True)
                emit('agr', 'SORTEO', broadcast=True)
                emit('pote',montoPote, broadcast=True)
                horaSorteo = sorteoTaquilla
                emit('limpiarSala','sala', broadcast=True)
            
            if horaSorteo == '12:30:00':
                sorteoNuevo = 5
                sorteoTaquilla = BuscarSorteo(sorteoNuevo)
                print('sorteo taquilla',sorteoTaquilla[0][0])
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(horaSorteo,montoPote,sorteoTaquilla[0][0])
                print('actualizo proximo',actualizoSorteo)
                time.sleep(10) #prueba enviar inicio sorteo
                emit('sorteo', sorteoTaquilla, broadcast=True)
                emit('agr', 'SORTEO', broadcast=True)
                emit('pote',montoPote, broadcast=True)
                horaSorteo = sorteoTaquilla
                emit('limpiarSala','sala', broadcast=True)
                
            if horaSorteo == '13:30:00':
                sorteoNuevo = 6
                sorteoTaquilla = BuscarSorteo(sorteoNuevo)
                print('sorteo taquilla',sorteoTaquilla[0][0])
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(horaSorteo,montoPote,sorteoTaquilla[0][0])
                print('actualizo proximo',actualizoSorteo)
                time.sleep(10) #prueba enviar inicio sorteo
                emit('sorteo', sorteoTaquilla, broadcast=True)
                emit('agr', 'SORTEO', broadcast=True)
                emit('pote',montoPote, broadcast=True)
                horaSorteo = sorteoTaquilla
                emit('limpiarSala','sala', broadcast=True)
                
            if horaSorteo == '14:30:00':
                sorteoNuevo = 7
                sorteoTaquilla = BuscarSorteo(sorteoNuevo)
                print('sorteo taquilla',sorteoTaquilla[0][0])
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(horaSorteo,montoPote,sorteoTaquilla[0][0])
                print('actualizo proximo',actualizoSorteo)
                time.sleep(10) #prueba enviar inicio sorteo
                emit('sorteo', sorteoTaquilla, broadcast=True)
                emit('agr', 'SORTEO', broadcast=True)
                emit('pote',montoPote, broadcast=True)
                horaSorteo = sorteoTaquilla
                emit('limpiarSala','sala', broadcast=True)
                
            if horaSorteo == '15:30:00':
                sorteoNuevo = 8
                sorteoTaquilla = BuscarSorteo(sorteoNuevo)
                print('sorteo taquilla',sorteoTaquilla[0][0])
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(horaSorteo,montoPote,sorteoTaquilla[0][0])
                print('actualizo proximo',actualizoSorteo)
                time.sleep(10) #prueba enviar inicio sorteo
                emit('sorteo', sorteoTaquilla, broadcast=True)
                emit('agr', 'SORTEO', broadcast=True)
                emit('pote',montoPote, broadcast=True)
                horaSorteo = sorteoTaquilla
                emit('limpiarSala','sala', broadcast=True)
                            
            if horaSorteo == '16:30:00':
                sorteoNuevo = 9
                sorteoTaquilla = BuscarSorteo(sorteoNuevo)
                print('sorteo taquilla',sorteoTaquilla[0][0])
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(horaSorteo,montoPote,sorteoTaquilla[0][0])
                print('actualizo proximo',actualizoSorteo)
                time.sleep(10) #prueba enviar inicio sorteo
                emit('sorteo', sorteoTaquilla, broadcast=True)
                emit('agr', 'SORTEO', broadcast=True)
                emit('pote',montoPote, broadcast=True)
                horaSorteo = sorteoTaquilla
                emit('limpiarSala','sala', broadcast=True)
                
            if horaSorteo == '19:30:00':
                sorteoNuevo = 10
                sorteoTaquilla = BuscarSorteo(sorteoNuevo)
                print('sorteo taquilla',sorteoTaquilla[0][0])
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(horaSorteo,montoPote,sorteoTaquilla[0][0])
                print('actualizo proximo',actualizoSorteo)
                time.sleep(10) #prueba enviar inicio sorteo
                emit('sorteo', sorteoTaquilla, broadcast=True)
                emit('agr', 'SORTEO', broadcast=True)
                emit('pote',montoPote, broadcast=True)
                horaSorteo = sorteoTaquilla
                emit('limpiarSala','sala', broadcast=True)
                
            if horaSorteo == '20:17:00':
                sorteoNuevo = 11
                sorteoTaquilla = BuscarSorteo(sorteoNuevo)
                print('sorteo taquilla',sorteoTaquilla[0][0])
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(horaSorteo,montoPote,sorteoTaquilla[0][0])
                print('actualizo proximo',actualizoSorteo)
                time.sleep(10) #prueba enviar inicio sorteo
                emit('sorteo', sorteoTaquilla, broadcast=True)
                emit('agr', 'SORTEO', broadcast=True)
                emit('pote',montoPote, broadcast=True)
                horaSorteo = sorteoTaquilla
                emit('limpiarSala','sala', broadcast=True)
                
            if horaSorteo == '21:00:00':
                sorteoNuevo = 1
                sorteoTaquilla = BuscarSorteo(sorteoNuevo)
                print('sorteo taquilla',sorteoTaquilla[0][0])
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(horaSorteo,montoPote,sorteoTaquilla[0][0])
                print('actualizo proximo',actualizoSorteo)
                time.sleep(10) #prueba enviar inicio sorteo
                emit('sorteo', sorteoTaquilla, broadcast=True)
                emit('agr', 'SORTEO', broadcast=True)
                emit('pote',montoPote, broadcast=True)
                horaSorteo = sorteoTaquilla
                emit('limpiarSala','sala', broadcast=True)
            
            print("BINGO BINGO,BINGO")
            print(cartonPremio)
            print(numeroUnicoEliminado)
            print('nuevo dia: ',nowDate)
            break 

#monitoreo de venta boletos lottoABC
@socketio.on('Compra')
def ventaBoletoLetra(compraLottoABC):
    while True:
        listaVenta = buscarVentaDia(nowDate)
        ventadiaria = []
        for items in listaVenta:
            diccVenta = {
                'serial': items[0],
                'opcion': items[4],
                'monto': items[3],
                'refPago':items[10]
            }
            ventadiaria.append(diccVenta)
        emit('compraLottoABC', ventadiaria, broadcast=True)
    
#solicito la vista para ver las ventas del dia 
@app.route('/ventaBoletoLetra', methods=['POST'])
def ventaBoletoLetra():
    return render_template('vistas/reporteVentaDiaria.html')

@app.route('/formRegister', methods=['POST'])
def formRegister():
    return render_template('login/register.html')

@app.route('/formLogin', methods=['POST'])
def formLogin():
    return render_template('login/login.html')

@app.route('/registro', methods=['POST'])
def registro():
    if request.method =='POST':
        try:
            # Validar que el formulario no esté vacío
            
            if not request.form.to_dict():
                return jsonify({
                    'success': False,
                    'message': 'Por favor complete todos los campos'
                }), 400  # Bad Request

            # Obtener datos del formulario
            nombre = request.form.get('nombre', '').strip()
            apellido = request.form.get('apellido', '').strip()
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            
            # Validar campos obligatorios
            if not all([nombre, apellido, username, password, email]):
                print('todos son obligatorios')
                return jsonify({
                    'success': False,
                    'message': 'Todos los campos son obligatorios excepto teléfono'
                }), 400
            
            # Validar contraseña mínima
            if len(password) < 8:
                print('todos son obligatorios 1')
                return jsonify({
                    'success': False,
                    'message': 'La contraseña debe tener al menos 8 caracteres'
                }), 400
            
            # Verificar si el usuario ya existe
            cursor = db.cursor()
            cursor.execute('SELECT username FROM usuarios WHERE username = %s', (username,))
            if cursor.fetchone():
                return jsonify({
                    'success': False,
                    'message': 'El nombre de usuario ya existe'
                }), 409  # Conflict
            
            # Crear hash de contraseña
            hashed_password = generate_password_hash(password)
            print('todos son obligatorios 3')
            # Insertar nuevo usuario
            cursor.execute(
                'INSERT INTO usuarios (nombre, apellido, username, password, email, phone) '
                'VALUES (%s, %s, %s, %s, %s, %s)',
                (nombre, apellido, username, hashed_password, email, phone)
            )
            db.commit()
            nombeApellido = nombre + ' ' + apellido
            validarCorreo = enviarCorreoVerificacion(email,nombeApellido,hashed_password)
            print('correo enviado',validarCorreo)
            return jsonify({
                'success': True,
                'message': 'Usuario registrado exitosamente',
            }), 201  # create successfully
            
        except Exception as e:
            db.rollback()
            print(f"Error en registro: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Ocurrió un error durante el registro'
            }), 500  # Internal Server Error
        

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()

            if not all([username, password]):
                return jsonify({
                    'success': False,
                    'message': 'Todos los campos son obligatorios'
                }), 400
            
            passwordHashDb = inicioSession(username)
            quest = check_password_hash(passwordHashDb[0]['password'], password)
            user_id = passwordHashDb[0]['id']
            
            if not quest:
                return jsonify({
                    'success': False,
                    'message': 'Usuario o contraseña incorrectos'
                }), 401
            
            # Establecer sesión (se marcará como permanente por el before_request)
            session['user_id'] = user_id

            return jsonify(
                success=True,
                message='Inicio de sesión exitoso',
                user_id=user_id,
                html=render_template('vistas/board.html')  # Renderiza el template como string
            ), 200  # OK
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
        
@app.route('/verifica/', methods=['GET'])
def verificar():
    token = request.args.get('id')
    
    if not token:
        return render_template('index.html', 
                            verification_result={
                                'status': False,
                                'message': 'Token no proporcionado'
                            })

    try:
        usuario = verificar_token_en_bd(token)
        
        if usuario:
            activar_usuario(usuario[0])
            return render_template('index.html', 
                                verification_result={
                                    'status': True,
                                    'message': '¡Cuenta activada correctamente!'
                                })
        else:
            return render_template('index.html', 
                                verification_result={
                                    'status': False,
                                    'message': 'Token inválido o expirado'
                                })

    except Exception as e:
        print(f"Error en verificación: {str(e)}")
        return render_template('index.html', 
                            verification_result={
                                'status': False,
                                'message': 'Error interno al verificar'
                            })


def verificar_token_en_bd(token):
    """Busca un usuario con el token/password"""
    try:
        cursor = db.cursor()
        
        # Consulta adaptada para MariaDB/MySQL
        query = """
            SELECT id, email 
            FROM usuarios 
            WHERE password = %s 
            AND activo = 1
        """
        cursor.execute(query, (token,))
        
        return cursor.fetchone()  # Retorna una tupla (id, email) o None
        
    except Exception as e:
        print(f"Error en consulta: {str(e)}")
        return None
    finally:
        cursor.close()


def activar_usuario(usuario_id):
    """Marca la cuenta como activa"""
    try:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE usuarios SET activo = 0 WHERE id = %s",
            (usuario_id,)
        )
        db.commit()
    except Exception as e:
        print(f"Error al activar usuario: {str(e)}")
        db.rollback()
    finally:
        cursor.close()

        
#Hora hora del sorteo cuando viene del back
@socketio.on('horaPendiente')
def horaSorteo(horaSorteo,montoPote):
    print('sorteo de: ',horaSorteo,'-',montoPote)
    sorteo = sorteopendiente()
    if montoPote =='':
        montoPote = sorteo[0][1]
    actualizoSorteo = sorteoReprogramado(horaSorteo,montoPote)
    datos={
        'horaSorteo':horaSorteo,
        'montoPote':montoPote
    }
    print(actualizoSorteo)
    emit('sorteo', datos, broadcast=True)
    
    
def alarma_horaria():
    while True:
        # Obtiene la hora actual
        ahora = datetime.now(tz_venezuela)
        print("hora es:", ahora.hour , ahora.minute,  ahora.second)
        # Comprueba si es la hora exacta (minuto y segundo son 0)
        if ahora.minute == 0 and ahora.second == 0:
            pote = sorteopendiente()
            sorteoPendiente = pote[0][0]
            pote = pote[0][1]
            print('pendente para ejecutar sorteo')
            hora_actual = str(ahora.hour )+':'+ str(ahora.minute) + ':' + str(ahora.second)
            print("¡Alarma! ¡Es hora del sorteo!", hora_actual)
            #sorteo letras
            if hora_actual == '07:0:0':
                sorteoNuevo = 1
                idSorteo = 8
                sorteoTaquilla = BuscarSorteoPendiente(sorteoNuevo)
                print(sorteoTaquilla)
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(hora_actual,montoPote,sorteoTaquilla[0]['sorteo'],idSorteo)
                sorteoletra = '07:00 am'
                sorteoLotto(sorteoletra,nowDate)
            if hora_actual == '13:0:0':
                sorteoNuevo = 2
                idSorteo = 1
                sorteoTaquilla = BuscarSorteoPendiente(sorteoNuevo)
                print(sorteoTaquilla)
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(hora_actual,montoPote,sorteoTaquilla[0]['sorteo'],idSorteo)
                sorteoletra = '01:00 pm'
                sorteoLotto(sorteoletra,nowDate)
            if hora_actual == '14:0:0':
                sorteoNuevo = 3
                idSorteo = 2
                sorteoTaquilla = BuscarSorteoPendiente(sorteoNuevo)
                print(sorteoTaquilla)
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(hora_actual,montoPote,sorteoTaquilla[0]['sorteo'],idSorteo)
                sorteoletra = '02:00 pm'
                sorteoLotto(sorteoletra,nowDate)
            if hora_actual == '15:56:0':
                sorteoNuevo = 4
                idSorteo = 3
                sorteoTaquilla = BuscarSorteoPendiente(sorteoNuevo)
                print(sorteoTaquilla)
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(hora_actual,montoPote,sorteoTaquilla[0]['sorteo'],idSorteo)
                sorteoletra = '03:00 pm'
                sorteoLotto(sorteoletra,nowDate) 
            if hora_actual == '16:0:0':
                sorteoNuevo = 5
                idSorteo = 4
                sorteoTaquilla = BuscarSorteoPendiente(sorteoNuevo)
                print(sorteoTaquilla)
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(hora_actual,montoPote,sorteoTaquilla[0]['sorteo'],idSorteo)
                sorteoletra = '04:00 pm'
                sorteoLotto(sorteoletra,nowDate)
            if hora_actual == '17:0:0':
                sorteoNuevo = 6
                idSorteo = 5
                sorteoTaquilla = BuscarSorteoPendiente(sorteoNuevo)
                print(sorteoTaquilla)
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(hora_actual,montoPote,sorteoTaquilla[0]['sorteo'],idSorteo)
                sorteoletra = '05:00 pm'
                sorteoLotto(sorteoletra,nowDate)
            if hora_actual == '18:0:0':
                sorteoNuevo = 7
                idSorteo = 6
                sorteoTaquilla = BuscarSorteoPendiente(sorteoNuevo)
                print(sorteoTaquilla)
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(hora_actual,montoPote,sorteoTaquilla[0]['sorteo'],idSorteo)
                sorteoletra = '06:00 pm' 
                sorteoLotto(sorteoletra,nowDate)
            if hora_actual == '19:0:0':
                sorteoNuevo = 9
                idSorteo = 7
                sorteoTaquilla = BuscarSorteoPendiente(sorteoNuevo)
                print(sorteoTaquilla)
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(hora_actual,montoPote,sorteoTaquilla[0]['sorteo'],idSorteo)
                sorteoletra = '07:00 pm' 
                sorteoLotto(sorteoletra,nowDate)
            if hora_actual == '20:0:0':
                sorteoNuevo = 10
                idSorteo = 9
                sorteoTaquilla = BuscarSorteoPendiente(sorteoNuevo)
                print(sorteoTaquilla)
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(hora_actual,montoPote,sorteoTaquilla[0]['sorteo'],idSorteo)
                sorteoletra = '08:00 pm' 
                sorteoLotto(sorteoletra,nowDate)
            if hora_actual == '21:0:0':
                sorteoNuevo = 8
                idSorteo = 10
                sorteoTaquilla = BuscarSorteoPendiente(sorteoNuevo)
                print(sorteoTaquilla)
                porcetajePote = int(pote) * 15 / 100
                montoPote = int(pote) + porcetajePote
                actualizoSorteo = updateSorteo(hora_actual,montoPote,sorteoTaquilla[0]['sorteo'],idSorteo)
                sorteoletra = '09:00 pm' 
                sorteoLotto(sorteoletra,nowDate)
                reset = resetSorteosDia()
                print(reset)
            time.sleep(60)  # Espera un minuto para evitar múltiples alarmas en el mismo minuto
        time.sleep(1)  # Espera un segundo antes de volver a comprobar
     
#Hora del servidor
@socketio.on('iniciarSistema')
def hora(iniciar):
    print(iniciar)
    hora_actual = ''
    if iniciar == 'Sistema Iniciado':
        # Obtener el pote y el sorteo pendiente
        pote = sorteopendiente()
        sorteoPendiente = pote[0][0]
        pote = pote[0][1]
    
        # asigno el valor del id del proximo sorteo 
        global contadorSorteo
        sorteoEjecutado = sorteosEjecutado()
        print('Cantidad sorteos ejecutados: ',sorteoEjecutado[0])
        if sorteoEjecutado[0] == 0:
            print('no se ha ejecutado sorteo')
            contadorSorteo += 1
        else:
            print('trae la cantidad de sorteos ejecutados y se asignan al contador')
            contadorSorteo = sorteoEjecutado[0]
            contadorSorteo += 1
        
        idSorteo = contadorSorteo #corresponde al id del sorteo actual
        contadorSorteo += 1
        sorteoNuevo = contadorSorteo #corresponde al id del nuevo sorteo
    
        print('contadorSorteo:',contadorSorteo)
        # Buscar la hora del sorteo
        buscarSorteoHora = BuscarSorteo()
        sorteoActual = None  # Inicializar la variable para el sorteo actual

        # Encontrar el sorteo actual basado en el id
        for itemSorteo in buscarSorteoHora:
            if itemSorteo['id'] == idSorteo:
                sorteoActual = itemSorteo['sorteo'] 
                break  # Salir del bucle una vez encontrado

        # Obtener el sorteo de taquilla pendiente
        sorteoTaquilla = BuscarSorteoPendiente(sorteoNuevo)
        print(sorteoTaquilla)

        # Calcular el porcentaje del pote
        porcentajePote = int(pote) * 15 / 100
        montoPote = int(pote) + porcentajePote
        print('sorteoTaquilla:',sorteoTaquilla)
        # Actualizar el sorteo
        actualizoSorteo = updateSorteo(hora_actual, montoPote, sorteoTaquilla[0]['sorteo'], idSorteo)
        # Realizar el sorteo de la letra
        sorteoletra = sorteoActual
        sorteoLotto(sorteoletra, nowDate)
        if sorteoletra == '09:00 pm':
            reset = resetSorteosDia()
            contadorSorteo = 0
            print(reset)
            
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/back', methods=['GET'])
def back():
    return render_template('vistas/iniciarSorteos.html')

@app.route('/buscarGanador', methods=['POST'])
def buscarGanador():
    serialGanador = ''
    serialG =''
    horaSorteo = request.form['horaSorteo']
    print(horaSorteo)
    vendidos = 0
    matrizCarton = []
    Carton = []
    cartonpremiar = buscarCartonesHoraSorteo(horaSorteo)
    for matriz in cartonpremiar:   
        matrizCarton.append(horaSorteo)
        nueva_cadenaB = ''.join(caracter for caracter in matriz[2] if caracter.isalnum() or caracter.isspace())
        matrizCarton.append(nueva_cadenaB)
        nueva_cadenaI = ''.join(caracter for caracter in matriz[3] if caracter.isalnum() or caracter.isspace())
        matrizCarton.append(nueva_cadenaI)
        nueva_cadenaN = ''.join(caracter for caracter in matriz[4] if caracter.isalnum() or caracter.isspace())
        matrizCarton.append(nueva_cadenaN)
        nueva_cadenaG = ''.join(caracter for caracter in matriz[5] if caracter.isalnum() or caracter.isspace())
        matrizCarton.append(nueva_cadenaG)
        nueva_cadenaO = ''.join(caracter for caracter in matriz[6] if caracter.isalnum() or caracter.isspace())
        matrizCarton.append(nueva_cadenaO) 
           
        opcionesCartonPremiado = buscarCartonesPremiadosHoraSorteo(horaSorteo)
        for matrizb in opcionesCartonPremiado:
            Carton.append(horaSorteo)
            nuevaB = ''.join(caracter for caracter in matrizb[1] if caracter.isalnum() or caracter.isspace())
            Carton.append(nuevaB)
            nuevaI = ''.join(caracter for caracter in matrizb[2] if caracter.isalnum() or caracter.isspace())
            Carton.append(nuevaI)
            nuevaN = ''.join(caracter for caracter in matrizb[3] if caracter.isalnum() or caracter.isspace())
            Carton.append(nuevaN)
            nuevaG = ''.join(caracter for caracter in matrizb[4] if caracter.isalnum() or caracter.isspace())
            Carton.append(nuevaG)
            nuevaO = ''.join(caracter for caracter in matrizb[5] if caracter.isalnum() or caracter.isspace())
            Carton.append(nuevaO)
            print('serialGanador',matriz) 
        if matrizCarton == Carton:
            serialG = matriz[0]  
    print('*****',serialG)           
    return jsonify({'serialGanador': serialG }) 

@app.route('/listarCartonePremiados', methods=['POST'])
def listarCartonesPremiados():
    print('Solicitud de cartones Premiados')
    opcionesJson = []
    opcionesCartonPremiado = buscarCartonesPremiados()
    horaSorteo=''
    for opcionesCarton in opcionesCartonPremiado:
        horaSorteo = opcionesCarton[0]
        cadenaB  = opcionesCarton[1]
        nueva_cadenab = ''.join(caracter for caracter in cadenaB if caracter.isalnum() or caracter.isspace())
        b = nueva_cadenab.split(' ')
                
        cadenaI  = opcionesCarton[2]
        nueva_cadenai = ''.join(caracter for caracter in cadenaI if caracter.isalnum() or caracter.isspace())
        i = nueva_cadenai.split(' ')
                
        cadenaN  = opcionesCarton[3]
        nueva_cadenaN = ''.join(caracter for caracter in cadenaN if caracter.isalnum() or caracter.isspace())
        n = nueva_cadenaN.split(' ')

        cadenaG  = opcionesCarton[4]
        nueva_cadenaG = ''.join(caracter for caracter in cadenaG if caracter.isalnum() or caracter.isspace())
        g = nueva_cadenaG.split(' ')
                
        cadenaO  = opcionesCarton[5]
        nueva_cadenaO = ''.join(caracter for caracter in cadenaO if caracter.isalnum() or caracter.isspace())
        o = nueva_cadenaO.split(' ')           
                
        opcion={
            'serial':'Resultado',
            'fecha': nowDate,
            'hora': horaSorteo,
            'B':b,
            'I':i,
            'N':n,
            'G':g,
            'O':o
        }
        opcionesJson.append(opcion)            
    return render_template('vistas/cartones.html',opcionesJson=opcionesJson)    

@app.route('/listaLetra', methods=['POST'])
def listaLetra():
    sorteoLetra = BuscarSorteo()
    opciones = opcionesJuego()
    print(sorteoLetra)
    #print('Opciones Juegos: ', opciones)
    return render_template('vistas/letras.html',opciones=opciones,sorteoLetra=sorteoLetra)
 
@app.route('/listarCartones', methods=['POST'])
def listarCartones():
    #consultar tabla numero unico por si estoy entrando a la sala y hay un sorteo en proceso
    print('Solicitud de Cartones')
    unico = numerosSorteo() 
    print('numeroUnico', unico)
    
    if unico:
        #cuando existe un sorteo activo
        print('hay sorteo activo: ', unico)
        return render_template('vistas/sorteoIniciado.html')
    else:    
        print('Solicitud de Cartones')
        sorteoPendiente = sorteopendiente()
        print('sorteo: ', sorteoPendiente)
        
        if not sorteoPendiente:
            return render_template('vistas/cartones.html', opcionesJson=[])
            
        sorteo = sorteoPendiente[0]
        vendidos = 0
        listCartones = buscarSerialCartones(vendidos, sorteo, nowDate)
        opcionesJson = []
        
        for numeroCarton in listCartones:    
            serialcarton = numeroCarton[0]
            horaSorteo = numeroCarton[1]
            FechaSorteo = numeroCarton[2]
            venta = numeroCarton[3]
            opcionesCarton = buscarCartones()
            
            if opcionesCarton and opcionesCarton[0][0] == serialcarton:
                # Procesar cada línea del cartón
                cadenas = []
                for i in range(1, 6):  # Para B, I, N, G, O
                    cadena = opcionesCarton[0][i]
                    nueva_cadena = ''.join(caracter for caracter in cadena if caracter.isalnum() or caracter.isspace())
                    cadenas.append(nueva_cadena.split())
                
                opcion = {
                    'serial': opcionesCarton[0][0],
                    'fecha': FechaSorteo,
                    'hora': horaSorteo,
                    'venta': venta,
                    'B': cadenas[0],
                    'I': cadenas[1],
                    'N': cadenas[2],
                    'G': cadenas[3],
                    'O': cadenas[4]
                }
                print('cartones:',opcion)
                opcionesJson.append(opcion)            
        
        return render_template('vistas/cartones.html', opcionesJson=opcionesJson)
    
    
"""GET Consultas"""
@app.route("/users/<user_id>")
def get_user(user_id):
    try:
        # Código que puede generar una excepción
        user = {"id":user_id,"name":"test","telefono":"9999-9998800"}
        return jsonify(user),200 
    except ValueError:
        # Manejo de la excepción específica
        error = {
            "codigo": "503",
            "mensajeError": "Servicio no disponible"
        }
        return jsonify(error),503
    
#iniciamos el sorteo
@app.route("/cantar")
def inicioSorteo():
    bolaCantada = cantarBola()
    bola = {
            "numero":bolaCantada[0]
            }
    return jsonify(bola),200 
   
 
"""POST Crear"""
#Crear Cartones Por Sorteo
@app.route("/crearCartones", methods=['POST'])
def crear_cartones():
    try: 
        cantidad=request.form['cantidad']
        horaSorteo = request.form['horaSorteo']
        cartones = matriz(int(cantidad),horaSorteo)
        return jsonify({
                'cantidad': cantidad
            }),201
    except ValueError:
        # Manejo de la excepción específica
        error = {
            "codigo": "503",
            "mensajeError": "Servicio no disponible"
        }
        return jsonify(error),503 

@app.route("/compraBoletoLetra", methods=['POST'])
def compraBoletoLetra():
    datosTicketLetra = request.form
    print('vendo la opcion',datosTicketLetra['monto'])
    #validamos que no se ingrese una referencia duplicada
    resultadoReferencia = buscarReferenciaLetra(datosTicketLetra['referencia'])
    if resultadoReferencia == []:
        sorteos = BuscarSorteo()
        for items in sorteos:
            if int(datosTicketLetra['sorteo']) == int(items['id']):
                sorteoOpcion = items['sorteo']
        print("Sorteo Opcion: ",sorteoOpcion)
        # Formatear la hora en formato 12H
        hora_12h = datetime.now(tz_venezuela)   
        print('Hora ticket: ',hora_12h.strftime("%I:%M:%S %p"))
        hora_12h = hora_12h.strftime("%I:%M:%S %p")
        serialTicket = generarTicketLetra(datosTicketLetra,hora_12h,nowDate)
        # Filtrar caracteres
        cadena_limpia = ''.join(filter(lambda x: x.isalnum() or x.isspace(), hora_12h)) 
        numeros = [serialTicket, cadena_limpia]
        # Convertir a cadenas y concatenar 
        resultado = ''.join(map(str, numeros))
        formatoSerial = resultado
        if serialTicket !='ok':
            return render_template('vistas/ticket.html',datosTicketLetra=datosTicketLetra,
                                   hora_12h=hora_12h,nowDate=nowDate,
                                   formatoSerial=formatoSerial,
                                   sorteoOpcion=sorteoOpcion )
    else:           
        return 'referencia duplicada'
#comprar boleto letra
@app.route("/comprarLetra", methods=['POST'])
def comprarLetra():
    try:
        global montoDisponible
        datosTicketLetra = request.form
        print('datos enviados: ',datosTicketLetra)
        resultadoReferencia = ""
        #validamos que no se ingrese una referencia duplicada
        resultadoReferencia = buscarReferenciaLetra(datosTicketLetra['referencia'])
        if resultadoReferencia == []:
           #Verificamos limites disponibles
            idjuegos = 1
            limiteOpciones = BuscarLimitesOpciones(idjuegos)
            print('Limite: ',limiteOpciones)
            #Verificamos los limites de la opcion jugada
            if int(datosTicketLetra['monto']) < limiteOpciones:
                print('entre a validar montos')
                #obtenemos la opcion Jugada y el sorteo
                opcionJugada = datosTicketLetra['opcionId']
                idSorteo = datosTicketLetra['sorteo']
                #sumar la venta de la opcion para la hora del sorteo
                montoOpcionVendida = sumaJugadasOpcion(opcionJugada,idSorteo,nowDate)
                print('total Jugado:', montoOpcionVendida[0])
                if  montoOpcionVendida[0] == None:
                    datos ={
                        'disponible':'procesar'
                    }
                    return datos 
                montoOpcionMayor = montoOpcionVendida[0] + int(datosTicketLetra['monto'])
                if montoOpcionMayor < limiteOpciones:
                    datos ={
                        'disponible':'procesar'
                    }
                    return datos
                        
                if montoOpcionMayor > limiteOpciones:
                    
                    montoDisponible = limiteOpciones - montoOpcionVendida[0] 
                    print(montoDisponible)
                    datos ={
                        'disponible':'disponible',
                        'monto':montoDisponible
                    }
                    return datos
                if montoOpcionMayor == limiteOpciones:
                    datos ={
                        'disponible':'procesar'
                    }
                    return datos                                
            else:
                #sumamos monto de la opcion jugada mas el monto opcion vendida
                #obtenemos la opcion Jugada y el sorteo
                opcionJugada = datosTicketLetra['opcionId']
                idSorteo = datosTicketLetra['sorteo']
                montoOpcionVendida = sumaJugadasOpcion(opcionJugada,idSorteo)
                print('monto 60: ',montoOpcionVendida[0])

                if montoOpcionVendida[0] == None and int(limiteOpciones) == int(datosTicketLetra['monto']):
                    datos ={
                        'disponible':'procesar'
                    }
                    return datos

                if int(montoOpcionVendida[0]) < int(limiteOpciones):
                    montoDisponible = montoOpcionVendida[0] + int(datosTicketLetra['monto'])
                    if montoDisponible > limiteOpciones:
                        datos ={
                            'disponible':'procesar',
                            'monto':montoDisponible
                        }
                        return datos 
                 
                if montoOpcionVendida[0] == None and int(datosTicketLetra['monto']) == limiteOpciones:
                    datos ={
                        'disponible':'procesar',
                        'monto':montoDisponible
                    }
                    return datos 
                   
                else: 
                    if montoOpcionVendida[0] ==60 and int(datosTicketLetra['monto']) == limiteOpciones:
                        datos ={
                        'disponible':'disponible',
                        'monto':0
                        }
                        return datos
        else:           
            return 'referencia duplicada'
    except ValueError:
        # Manejo de la excepción específica
        error = {
            "codigo": "503",
            "mensajeError": "Servicio no disponible"
        }
        return jsonify(error),503
    
#comprar Boleto Bingo
@app.route("/compraBoleto", methods=['POST'])
def compra_boletos():
    try:
        #compramos el boleto
        referenciaExiste = []
        datosBoleto = request.form
        #consultar si la referencia bancaria existe
        referencia = datosBoleto["referencia"]
        referenciaExiste = buscarReferencia(referencia)
        print('existe referencia',referenciaExiste)
        if referenciaExiste == []:
            compra = compraBoleto(datosBoleto)
            if compra['venta'] == 'Rechazada':
                print('resultado compra: ',compra['venta'])
                return render_template('vistas/ventaRechazada.html')
            else:
                serialcarton = datosBoleto["serialBoleto"]
                #buscamos el boleto comprado
                opcionesJson = []
                opcionesCarton = buscarCartones(serialcarton)
                listCartones = buscarSerialCartonesVendido(serialcarton)
                print(listCartones)
                horaSorteo = listCartones[0][1]
                fechaSorteo = listCartones[0][2]
                venta = listCartones[0][3]
                print(opcionesCarton[0][0])
                print(serialcarton)
                if int(opcionesCarton[0][0]) == int(serialcarton):
                    cadenaB  = opcionesCarton[0][1]
                    nueva_cadenab = ''.join(caracter for caracter in cadenaB if caracter.isalnum() or caracter.isspace())
                    b = nueva_cadenab.split(' ')
                                    
                    cadenaI  = opcionesCarton[0][2]
                    nueva_cadenai = ''.join(caracter for caracter in cadenaI if caracter.isalnum() or caracter.isspace())
                    i = nueva_cadenai.split(' ')
                        
                    cadenaN  = opcionesCarton[0][3]
                    nueva_cadenaN = ''.join(caracter for caracter in cadenaN if caracter.isalnum() or caracter.isspace())
                    n = nueva_cadenaN.split(' ')

                    cadenaG  = opcionesCarton[0][4]
                    nueva_cadenaG = ''.join(caracter for caracter in cadenaG if caracter.isalnum() or caracter.isspace())
                    g = nueva_cadenaG.split(' ')
                        
                    cadenaO  = opcionesCarton[0][5]
                    nueva_cadenaO = ''.join(caracter for caracter in cadenaO if caracter.isalnum() or caracter.isspace())
                    o = nueva_cadenaO.split(' ')           
                        
                    opcion={
                        'serial':opcionesCarton[0][0],
                        'fecha': fechaSorteo,
                        'hora': horaSorteo,
                        'venta':venta,
                        'B':b,
                        'I':i,
                        'N':n,
                        'G':g,
                        'O':o
                    }
                    opcionesJson.append(opcion)  
                    print('Compra Procesada') 
                    vendidos = 1
                    listCartonesVendidos = buscarTotalCartonesVendidos1(vendidos,horaSorteo,nowDate)
                    totalVendidos = listCartonesVendidos[0][0]
                    print('total Vendidos',totalVendidos)          
                return render_template('vistas/cartones.html',opcionesJson=opcionesJson)
        else:
            return render_template('vistas/referenciaExiste.html')  
         #///////////////////////////    
    except ValueError:
        # Manejo de la excepción específica
        error = {
            "codigo": "503",
            "mensajeError": "Servicio no disponible"
        }
        return jsonify(error),503
    
# Sala de Juego
@app.route("/salaJuego", methods=['POST'])
def salaJuego():
    try: 
        #consultar  tabla numero unico por si estoy entrando a la sala y hay un sorteo en proceso
        unico=[]
        unico = numerosSorteo() 
        sorteo = sorteopendiente()
        sorteoPendiente = sorteo[0][0]
        pote = sorteo[0][1]
        print('numeroUnico',unico)
        if unico !=[]:
            #cuando existe un sorteo activo
            print('hay sorteo activo: ',unico,sorteo)
            return render_template('vistas/sorteoIniciado.html',unico=unico,sorteo=sorteoPendiente,pote=pote)
        else:
            #cundo no hay sorteo iniciado se envia numero unico vacio para no danar 
            # la logica de la vista.
            vendidos = 1
            listCartonesVendidos = buscarTotalCartonesVendidos(vendidos,sorteo,nowDate)
            totalVendidos = listCartonesVendidos[0][0]
            return render_template('vistas/sala.html',unico=unico,sorteo=sorteoPendiente,pote=pote,totalVendidos=totalVendidos)
        
    except ValueError: 
        # Manejo de la excepción específica
        error = {
            "codigo": "503",
            "mensajeError": "Servicio no disponible"
        }
        return jsonify(error),503 

#letra cantada 
@app.route("/letraCantada", methods=['POST'])
def letraCantada():
    try:
        print('sorteo Letra')
        listarResultadoLetra = resultadoLetra(nowDate)
        return render_template('vistas/letra.html',listarResultadoLetra =listarResultadoLetra)
    except ValueError: 
        # Manejo de la excepción específica
        error = {
            "codigo": "503",
            "mensajeError": "Servicio no disponible"
        }
        return jsonify(error),503 
        
#Hora del servidor
@socketio.on('boletoventa')
def contarCartonesVendidos(totalVendidos):
    print('solicito',totalVendidos)
    sorteo = sorteopendiente()
    sorteoPendiente = sorteo[0][0]
    print('sorteo pendiente',sorteoPendiente)
    vendidos = 1
    listCartonesVendidos = buscarTotalCartonesVendidos1(vendidos,sorteoPendiente,nowDate)
    totalVendidos = listCartonesVendidos[0][0]
    print('total vendido', totalVendidos)
    emit('boletoventa', totalVendidos, broadcast=True)
       
@app.route("/efectoAparecerBola", methods=['POST'])    
def efectoAparecerBola():
    time.sleep(5) 
    contador = 0  # Inicializamos el contador en 0 
    return render_template('vistas/bolaNueva.html',contar=contador)
        
#code
"""Hora Fecha"""
def fecha():
    """Fecha/Hora"""
    
    print(" * Servidor Iniciado")
    print(" * Fecha / Hora: ",now)
    print(' * conectado DB ')
    return now
 
if __name__=="__main__": 
    #app.run(debug=True)
    #socketio.run(app)
    socketio.run(app,'10.0.0.40',80)
    fechaHora = fecha()
    #socketio.run(app,'10.0.0.3',80)
    #app.run('10.0.0.2', 80, debug=True)