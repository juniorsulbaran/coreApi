import random
#Generamos aleatorios
def cantarBola():
    aleatorios = random.sample(range(1,75),1)
    #numero letra B
    if aleatorios[0] >= 1 and aleatorios[0] <= 15:
        print("B :",aleatorios[0])
        return aleatorios
    #numero letra I
    if int(aleatorios[0]) >=16 and int(aleatorios[0]) <= 30:
        print("I:",aleatorios[0])
        return aleatorios
    #numero letra N
    if int(aleatorios[0]) >=31 and int(aleatorios[0]) <= 45:
        print("N:",aleatorios[0])
        return aleatorios
    #numero letra G
    if int(aleatorios[0]) >=46 and int(aleatorios[0]) <= 60:
        print("G:",aleatorios[0])
        return aleatorios
    #numero letra O
    if int(aleatorios[0]) >=61 and int(aleatorios[0]) <= 75:
        print("G:",aleatorios[0])
        return aleatorios