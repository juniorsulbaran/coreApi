# funcione para crear los cartones de bingo

#importamos librerias
import random
import pandas as pd
import datetime
from consultasdb import guardarCartone
import time
import string
now = datetime.datetime.now()

#numero unico 
def unico(x,l):
    esunico = True
    for i in range(len(l)):
        if x ==l[i]:
            esunico=False
            break
    return esunico
#matriz de numero
def numeroMatriz(menor,mayor):
    l=[]
    j=0
    while j<5:
        x = random.randint(menor,mayor)
        if unico(x,l):
            l.append(x)
            j+=1
    return l
#Generar Cartones por fecha y hora
def matriz(cantidad,horaSorteo):
    cartones =[]
    cont = 0
    
    fecha = now.strftime("%d-%m-%Y")
    
    while cont<cantidad:
        cont+=1
        B1 = numeroMatriz(1,15)
        I2 = numeroMatriz(16,30)
        N3 = numeroMatriz(31,45)
        G4 = numeroMatriz(46,60)
        O5 = numeroMatriz(61,75)
        carton = {
            "B":B1,
            "C":I2,
            "D":N3,
            "E":G4,
            "F":O5, 
            "serialTicket":cont,
            "horaSorteo": horaSorteo,
            "fecha":fecha
        }
        guardarCartone(carton)
        cartones.append(carton)
    return cartones
    