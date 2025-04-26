#********************************************************************************************************
#  Aplicación:    Bingo Virtual MySQL                                                                   # 
#  Desarrollador: Junior Sulbaran                                                                       #
#  Empresa:       ADFSoft                                                                               #
#  Año:           2024                                                                                  #
#*******************************************************************************************************# 

from flask import Flask, jsonify, request,render_template,redirect,url_for,flash
import mysql.connector
from conexiones import *
import json

#consulto los soteos ejecutados para obtener el id del proximo sorteo
def sorteosEjecutado():
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM sorteos where status = 1")
    result = mycursor.fetchall()
    mydb.close
    print('result:', result)   
    return result[0]

# buscamos la venta del dia en la tabla ticketvendido
def buscarVentaDia(nowDate):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ticketvendido where fecha = '%s'" % nowDate)
    result = mycursor.fetchall()
    mydb.close
    #print('result:', result)   
    return result

def guardoLetraGanadora(letra,sorteoletra,nowDate):
    #Guarda el resultado de la letra ganadora
    nombreTabla1 = "resultadoletra"
    mydb = conectar_base_datos()
    mycursor1 = mydb.cursor()
    sql1 = "INSERT INTO "+ nombreTabla1 + " (letra,hora,fecha) VALUES (%s,%s,%s)"
    val1 = (letra,sorteoletra,nowDate)
    mycursor1.execute(sql1,val1)
    mydb.commit()
    mydb.close()


#Consultamos la tabla resultadoletra
def resultadoLetra(nowDate):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM resultadoletra WHERE fecha = '%s'" % nowDate)
    result = mycursor.fetchall()
    mydb.close()
    if result ==[]:
        result = {
            'resultado':'Sin resultados'
            }
    return result

# Guardar los cartones creados por sorteo
def guardarCartone(carton):
    mydb = conectar_base_datos()
    #lista de datos para crear nuevo Usuarios AppIngestaWeb
    horaSorteo = carton['horaSorteo']
    fechaSorteo = carton['fecha']
    vendido = 0

    b = ', '.join(map(str, carton['B']))
    i = ', '.join(map(str, carton['C']))
    n = ', '.join(map(str, carton['D']))
    g = ', '.join(map(str, carton['E']))
    o = ', '.join(map(str, carton['F']))
    nombreTabla = "cartones"
    mycursor = mydb.cursor()
    sql = "INSERT INTO "+ nombreTabla + " (horaSorteo,fechaSorteo,vendido,B,I,N,G,O) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (horaSorteo,fechaSorteo,vendido,b,i,n,g,o)
    mycursor.execute(sql,val)
    mydb.commit()
    mydb.close()

#compra de boleto
def compraBoleto(datosBoletos):
    #datos de pago movil para enviar premio
    cedulaPremio = datosBoletos["cedulaPremio"]
    bancoPremio = datosBoletos["bancoPremio"]
    # Este parametro hace referencia al numero de pago movil y contacto
    correo = datosBoletos["telefonoPremio"]
    telefono = datosBoletos["telefonoPremio"]

    banco = datosBoletos["Banco"]
    serialBoleto = datosBoletos["serialBoleto"]
    monto = datosBoletos["monto"]
    referencia = datosBoletos["referencia"]
    nombreTabla = "boletovendido"

    #verifica que el boleto no se a vendido
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT vendido FROM cartones WHERE id = '%s'" % serialBoleto)
    result = mycursor.fetchall()
    if result[0][0] == 0:
        mycursor = mydb.cursor()
        sql = "INSERT INTO "+ nombreTabla + " (serialBoleto,correo,referencia,monto,banco) VALUES (%s,%s,%s,%s,%s)"
        val = (serialBoleto,correo,referencia,monto,banco)
        mycursor.execute(sql,val)

        # Definir la consulta SQL con variables
        vendido = 1
        consulta = "UPDATE cartones SET vendido = %s WHERE id = %s"
        datos = (vendido, serialBoleto)
        # Ejecutar la consulta con las variables
        mycursor.execute(consulta, datos)
        # Hacer commit para aplicar los cambios
        mydb.commit()
        mydb.close()
        respuesta = {
            "venta":"vendido"
        }
        guardoPagomovilPremio(cedulaPremio,bancoPremio,telefono)
        return respuesta
    else:
        respuesta = {
            "venta":"Rechazada"
        }
        return respuesta

def buscarSerialCartones(vendidos,sorteo,nowDate):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id,horaSorteo,FechaSorteo,vendido FROM cartones WHERE vendido = '%s' and FechaSorteo = '%s' and horaSorteo = '%s' " % (vendidos,nowDate,sorteo[0]))
    result = mycursor.fetchall()
    mydb.close()
    return result

def buscarTotalCartonesVendidos(vendidos,sorteo,nowDate):
    print('No hay sorteo activo',sorteo[0][0])
    print(nowDate)
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(id) AS TotalRegistros FROM cartones WHERE vendido = '%s' and FechaSorteo = '%s' and horaSorteo = '%s' " % (vendidos,nowDate,sorteo[0][0]))
    result = mycursor.fetchall()
    mydb.close()
    return result

def buscarTotalCartonesVendidos1(vendidos,horaSorteo,nowDate):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(id) AS TotalRegistros FROM cartones WHERE vendido = '%s' and FechaSorteo = '%s' and horaSorteo = '%s' " % (vendidos,nowDate,horaSorteo))
    result = mycursor.fetchall()
    mydb.close()
    return result

def buscarSerialCartonesVendido(serialcarton):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id,horaSorteo,FechaSorteo,vendido FROM cartones WHERE id = '%s'" % serialcarton)
    result = mycursor.fetchall()
    mydb.close()
    return result

def buscarReferencia(referencia):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT referencia FROM boletovendido WHERE referencia = '%s'" % referencia)
    result = mycursor.fetchall()
    mydb.close()
    print(result)
    return result

def sumaJugadasOpcion(opcionJugada,idSorteo):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT SUM(monto) FROM ticketvendido WHERE idjuego and sorteo = '%s'" % opcionJugada)


def buscarReferenciaLetra(referencia):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT referencia FROM ticketvendido WHERE referencia = '%s'" % referencia)
    result = mycursor.fetchall()
    mydb.close()
    print('referencia ticket: ',result)
    return result

def sumaJugadasOpcion(opcionJugada, idSorteo,nowDate):
    # Asegúrate de convertir los parámetros a enteros dentro de la función
    opcionJugada = int(opcionJugada)
    idSorteo = int(idSorteo)
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    # Corregir la consulta SQL
    query = "SELECT SUM(monto)  FROM ticketvendido WHERE idopcion = %s AND idsorteo = %s AND fecha = %s"
    mycursor.execute(query, (opcionJugada, idSorteo,nowDate))
    result = mycursor.fetchall()  # Obtener un solo resultado
    mydb.close()  # Asegúrate de llamar a close() como un método
    print('Suma jugadas:', result)
    # Retornar la suma o 0 si no hay resultados
    return result[0] if result and result[0] is not None else 0


def buscarCartones(serialcarton):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id,B,I,N,G,O FROM cartones WHERE id = '%s'" % serialcarton)
    result = mycursor.fetchall()
    mydb.close()
    return result

def buscarCartonesPremiar(serialcarton):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT horaSorteo,B,I,N,G,O FROM cartones WHERE id = '%s'" % serialcarton)
    result = mycursor.fetchall()
    mydb.close()
    return result

def buscarCartonesHoraSorteo(horaSorteo):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id,horaSorteo,B,I,N,G,O FROM cartones WHERE horaSorteo = '%s'" % horaSorteo)
    result = mycursor.fetchall()
    mydb.close()
    return result

def buscarCartonesPremiarHoraSorteo(horaSorteo):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT horaSorteo,B,I,N,G,O FROM cartones WHERE horaSorteo = '%s'" % horaSorteo)
    result = mycursor.fetchall()
    mydb.close()
    return result

def buscarCartones(serialcarton):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id,B,I,N,G,O FROM cartones WHERE id = '%s'" % serialcarton)
    result = mycursor.fetchall()
    mydb.close()
    return result

def buscarCartonesPremiados():
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT horaSorteo,B,I,N,G,O FROM cartonpremiado" )
    result = mycursor.fetchall()
    mydb.close()
    return result

def buscarCartonesPremiadosHoraSorteo(horaSorteo):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT horaSorteo,B,I,N,G,O FROM cartonpremiado WHERE horaSorteo = '%s'" % horaSorteo )
    result = mycursor.fetchall()
    mydb.close()
    return result

def guardoPagomovilPremio(cedulaPremio,bancoPremio,telefono):
    #guardo los datos del pago movil para pagar el
    nombreTabla1 = "pagomovilpremio"
    mydb = conectar_base_datos()
    mycursor1 = mydb.cursor()
    sql1 = "INSERT INTO "+ nombreTabla1 + " (cedulaPremio,bancoPremio,telefono) VALUES (%s,%s,%s)"
    val1 = (cedulaPremio,bancoPremio,telefono)
    mycursor1.execute(sql1,val1)
    mydb.commit()

def numeroUnico(numero):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT numerosorteado FROM numerounico WHERE numerosorteado = '%s'" % numero)
    result = mycursor.fetchall()
    mydb.close()
    return result

def contador():
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM numerounico")
    result = mycursor.fetchall()
    mydb.close()
    contar = result
    return contar

def BuscarLimitesOpciones(idjuego):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM limiteopciones WHERE idjuego = '%s'" % idjuego)
    result = mycursor.fetchall()
    mydb.close()
    return result[0][1]

def guardoNumeroSorteado(numero):
    #guardo los datos del pago movil para pagar el
    nombreTabla1 = "numerounico"
    mydb = conectar_base_datos()
    mycursor1 = mydb.cursor()
    sql1 = "INSERT INTO "+ nombreTabla1 + " (numerosorteado) VALUES (%s)"
    mycursor1.execute(sql1,(numero,))
    mydb.commit()

def borrarTablaNumeroUnico():
    mydb = conectar_base_datos()
    # Crear un cursor para ejecutar consultas
    cursor = mydb.cursor()
    # Ejecutar la consulta para eliminar registros
    consulta = "DELETE FROM numerounico WHERE numerosorteado"
    cursor.execute(consulta)
    # Confirmar la eliminación
    mydb.commit()
    # Cerrar el cursor y la conexión
    cursor.close()
    return 'Registros Eliminados'

#guardamos el clon del carton ganador
def cartonPremiado(horaSorteo,nowDate,premioB,premioI,premioN,premioG,premioO):
    # Convert the list to a string
    premioB = ', '.join(map(str, premioB))
    premioI = ', '.join(map(str, premioI))
    premioN = ', '.join(map(str, premioN))
    premioG = ', '.join(map(str, premioG))
    premioO = ', '.join(map(str, premioO))
    nombreTabla1 = "cartonpremiado"
    mydb = conectar_base_datos()
    mycursor1 = mydb.cursor()
    sql1 = "INSERT INTO "+ nombreTabla1 + " (horaSorteo,FechaSorteo,B,I,N,G,O) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    val1 = (horaSorteo,nowDate,premioB,premioI,premioN,premioG,premioO)
    mycursor1.execute(sql1,val1)
    mydb.commit()
    return 'guardado Con exito'

#actualizamos los sorteos
def updateSorteo(horaSorteo,pote,sorteoTaquilla,idSorteo):
        mydb = conectar_base_datos()
        mycursor = mydb.cursor()
        jugado = 1
        consulta = "UPDATE sorteos SET status = %s WHERE id = %s"
        datos = (jugado, idSorteo)
        # Ejecutar la consulta con las variables
        mycursor.execute(consulta, datos)
        # Hacer commit para aplicar los cambios
        mydb.commit()

        mycursor = mydb.cursor()
        id = 1
        consulta = "UPDATE sorteopendiente SET horaSorteo = %s, pote = %s WHERE id = %s"
        datos = (sorteoTaquilla,pote, id)
        # Ejecutar la consulta con las variables
        mycursor.execute(consulta, datos)
        # Hacer commit para aplicar los cambios
        mydb.commit()
        mydb.close()
        return 'Sorteos Actualizado'

#reprogramo sorteo que no se ejecuto
def sorteoReprogramado(sorteoTaquilla,pote):
        mydb = conectar_base_datos()
        mycursor = mydb.cursor()
        id = 1
        consulta = "UPDATE sorteopendiente SET horaSorteo = %s, pote = %s WHERE id = %s"
        datos = (sorteoTaquilla,pote, id)
        # Ejecutar la consulta con las variables
        mycursor.execute(consulta, datos)
        # Hacer commit para aplicar los cambios
        mydb.commit()
        mydb.close()
        return 'Sorteos Actualizado'

def resetSorteosDia():
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    status = 0
    consulta = "UPDATE sorteos SET status = %s WHERE status = %s"
    datos = (status,1)
    mycursor.execute(consulta, datos)
    # Hacer commit para aplicar los cambios
    mydb.commit()
    mydb.close()
    return 'Sorteos Inicializados'

#consulto el nuevo sorteo para enviar a la taquilla
def BuscarSorteo():
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sorteos")
    result = mycursor.fetchall()
    mydb.close
    dicSorteo=''
    ListaSorteo=[]
    print('Lista Sorteos: ',result)
    for items in result:
        dicSorteo = {
            'id': items[0],
            'sorteo': items[1],
            'status': items[2]
        }
        ListaSorteo.append(dicSorteo)
    return ListaSorteo

#conulto el nuevo sorteo para enviar a la taquilla
def BuscarSorteoPendiente(sorteoNuevo):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sorteos WHERE id = '%s'" % sorteoNuevo)
    result = mycursor.fetchall()
    mydb.close()
    dicSorteo=''
    ListaSorteo=[]
    print('Lista Sorteos: ',result)
    for items in result:
        dicSorteo = {
            'id': items[0],
            'sorteo': items[1],
            'status': items[2]
        }
        ListaSorteo.append(dicSorteo)
    return ListaSorteo



def generarTicketLetra(datosTicketLetra,hora_12h,nowDate):
    referencia = ''
    sorteo = datosTicketLetra['sorteo']
    referencia = datosTicketLetra['referencia']
    print('Referencia GenerarTicket: ',referencia)
    monto = datosTicketLetra['monto']
    idjuego = 1
    opcionId = datosTicketLetra['opcionId']
    opcionNombre = datosTicketLetra['opcionNombre']
    fecha = nowDate
    hora = hora_12h
    idVendedor = datosTicketLetra['idVendedor']
    status = 1 #vendido

    nombreTabla1 = "ticketvendido"
    mydb = conectar_base_datos()
    mycursor1 = mydb.cursor()
    sql1 = "INSERT INTO "+ nombreTabla1 + "(idjuego,idopcion,opcionNombre,monto,idsorteo,fecha,hora,referencia,idvendedor,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val1 = (idjuego,opcionId,opcionNombre,monto,sorteo,fecha,hora,referencia,idVendedor,status)
    mycursor1.execute(sql1,val1)
    mydb.commit()

    #obtenemos el ultimo registro de la tababla para enviar el serial del ticket
    mycursor1.execute("SELECT * FROM "+ nombreTabla1 + " ORDER BY id DESC LIMIT 1")
    ultimo_registro = mycursor1.fetchone()  # Obtener el último registro
    mydb.close()
    return ultimo_registro[0]


#Consultamos la tabla numero unico por si hay sorteo activo
def numerosSorteo():
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT numerosorteado FROM numerounico")
    result = mycursor.fetchall()
    mydb.close()
    return result

#consultamos el sorteo pendiente
def sorteopendiente():
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT horaSorteo,pote FROM sorteopendiente")
    result = mycursor.fetchall()
    mydb.close()
    return result

def opcionesJuego():
    mydb = conectar_base_datos()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM opcionesjuegos" )
    result = mycursor.fetchall()
    mydb.close()
    dicletra=''
    opciones=[]
    for items in result:
        dicletra = {
            'id': items[0],
            'idJuegos': items[1],
            'nombre': items[2]
        }
        opciones.append(dicletra)
    print(opciones)
    return result

def inicioSession(username):
    mydb = conectar_base_datos()
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute('SELECT id, password FROM usuarios WHERE username = %s', (username,))
    result = mycursor.fetchall()
    mydb.close()
    return result