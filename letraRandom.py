import random
# Variable para almacenar el último número generado
ultimo_numero = None

# Generamos aleatorios
def cantarLetra():
    global ultimo_numero  # Usamos la variable global para acceder al último número

    # Generar un nuevo número aleatorio que no sea igual al último
    while True:
        aleatorios = random.sample(range(1, 28), 1)[0]  # Genera un número aleatorio entre 1 y 27
        if aleatorios != ultimo_numero:  # Verifica que no sea igual al último número
            ultimo_numero = aleatorios  # Actualiza el último número
            break  # Sale del bucle si se genera un número válido

    # Mapeo de números a letras
    letras = {
        1: "A", 2: "B", 3: "C", 4: "D", 5: "E",
        6: "F", 7: "G", 8: "H", 9: "I", 10: "J",
        11: "K", 12: "L", 13: "M", 14: "N", 15: "Ñ",
        16: "O", 17: "P", 18: "Q", 19: "R", 20: "S",
        21: "T", 22: "U", 23: "V", 24: "W", 25: "X",
        26: "Y", 27: "Z"
    }

    # Obtener la letra correspondiente al número generado
    letra = letras.get(aleatorios)
    print("letra :", ultimo_numero)
    print("Letra Premiada:", letra)
    return letra
        
        