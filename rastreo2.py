
import os
import re

#Modela el objeto línea y sus atributos necesarios para realizar el rastreo
class linea():
    def __init__(self, nombre, ubicacion, temperatura):
        self.nombre = nombre #nombre de la línea
        self.ubicacion = ubicacion  #lista de ubicaciones
        self.temperatura = temperatura #lista de temperaturas

def reporteError(mensaje):
    print(mensaje)   
    
#Verifica si la temperatura de un punto adyacente esta fuera de rango
def verificarTemperatura(temperatura : float):
    if  temperatura > 26 or  temperatura < 22:
        print("La temperatura de esta linea tambien esta fuera de rango" + str(temperatura))
        return temperatura
    return 0
#Calcula el promedio de los 3 puntos adyacentes fuera de rango
def calcularPromedio(listapc):
    suma = 0
    for pc in listapc:
        suma = suma + int(pc)
    return suma / len(listapc)



def verificarNPC(n:int):
    if n >= 3:
        return True
    return False

#obtiene la ruta en donde estan ubicados los archivos con los resultados de comsol
try:
    ruta = ''
    # ruta = os.path.abspath(ruta)+'/resultados' #Ruta linux
    ruta = os.path.abspath(ruta)+'\\Resultados' #Ruta win
except:
    reporteError('Error al obtener la ruta')


lineas = [] #Lista de lineas
listaUbicaciones = [] #lista ubicaciones de cada punto en la línea
listaTemperaturas = [] #lista temperaturas de cada punto en la línea

#Leerá los 36 archivos de la carpeta resultados y guardará la informacion necesaria en la lista lineas 
for x in range(1,2):
    nombreArchivoLinea = str(x) + '.txt' 
    #Lee el archivo y guarda su informacion completa en la variable data
    try:
        f = open (ruta+'/'+nombreArchivoLinea,'r+')
        data = f.read()
        f.close()
    except:
        reporteError('Error al leer el archivo')
        
    #Transforma data en una lista de líneas del archivo 
    data = re.split('\n',data)
    
    #Elimina de la lista las primeras 8 líneas
    for y in range(7):
        data.pop(0)
    
    #Obtiene la ubicación y la temperatura y las guarda en su respectiva lista
    for d in data:
        datos = d.split();    
        listaUbicaciones.append(float(datos[0])) 
        listaTemperaturas.append(float(datos[1])) 
        
    #Inserta un nuevo objeto linea instanciado con los datos obtenidos en la lista lineas
    lineas.append(linea(x, listaUbicaciones, listaTemperaturas))
    
for l in lineas:
    print("Lista " + str(l.nombre) + "\n")
    for x in range(len(l.ubicacion)):        
        print(str(l.ubicacion[x]) + "-----" + str(l.temperatura[x]) ) 
    
k = 0 # k: índice del punto analizado.
pc =  False  # pc: punto crítico boolean
npc = 0 # npc: número de punto crítico 
tp = 0 # tp: temperatura promedio
tpm = 0 # tpm: temperatura promedio máxima 
listapc = [] # pc1, pc2, pc3: punto crítico 1, 2 y 3. (temperatura)
punto = 0 

#Buscar la ubicacion de la zona de calor de la seccion 1[1-12]
for x in range(1,13):
    for t in lineas[x].temperatura:
        i = t.index()
        if verificarTemperatura(t) != 0:
            pc = True
            npc = npc + 1
            listapc.append(t)
            #!!!!!!!!Revisar lo que va  a pasar cuando estes en el ultimo punto de la lista, porque ya no habra dos siguientes puntos 
            if i <= (len(lineas[x].temperatura)-2):
                if verificarTemperatura(lineas[x].temperatura[i+1]) != 0:
                    npc = npc +1
                    listapc.append(t)
                if verificarTemperatura(lineas[x].temperatura[i+2]) != 0:
                    npc = npc +1
                    listapc.append(t)
            #11.Esquina inferior izquierda: 1; arriba, derecha. (+1, +3)
            if x == 1:
                if verificarTemperatura(lineas[x+1].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
                if verificarTemperatura(lineas[x+3].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
            #10.Esquina superior izquierda: 3; abajo, derecha. (-1, +3)
            elif x == 3:
                if verificarTemperatura(lineas[x-1].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
                if verificarTemperatura(lineas[x+3].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
            #9.Lateral izquierdo: 2; arriba, abajo, derecha. (+1, -1, +3)
            elif x == 2:
                if verificarTemperatura(lineas[x+1].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
                if verificarTemperatura(lineas[x-1].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
                if verificarTemperatura(lineas[x-3].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
            #3.	Superior: 6, 9, 12, 15, 18, 21; abajo, izquierda, derecha. (-1, -3, +3)
            elif x == 6 or x == 9 or x == 12 or x == 15 or x == 18 or x == 21:
                if verificarTemperatura(lineas[x-1].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
                if verificarTemperatura(lineas[x-3].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
                if verificarTemperatura(lineas[x+3].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
            #1.	Centro: 5, 8, 11, 14, 17, 20; arriba, abajo, izquierda, derecha. (+1,-1,-3, +3)
            elif  x == 5 or x == 8 or x == 11 or x == 14 or x == 17 or x == 20 :
                if verificarTemperatura(lineas[x+1].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
                if verificarTemperatura(lineas[x-1].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
                if verificarTemperatura(lineas[x-3].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
                if verificarTemperatura(lineas[x+3].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
            #7.	Inferior: 4, 7, 10, 13, 16, 19; arriba, izquierda, derecha. (+1,-3, +3)
            elif  x == 4 or x == 7 or x == 10 or x == 13 or x == 16 or x == 19:
                if verificarTemperatura(lineas[x+1].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
                if verificarTemperatura(lineas[x-3].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
                if verificarTemperatura(lineas[x+3].temperatura[i]) != 0:
                    npc = npc +1
                    listapc.append(t)
        tp = calcularPromedio(listapc)
        if tpm < tp:
            punto = lineas[x].ubicacion[i]
            tpm = tp
        pc = False
        npc = 0
        listapc.clear()
        
            
    #cuando termine de recorrer todas las lineas de la seccion uno, tendremos dos resultados importantes que son;
    #la tpm: la temperatura promedio maxima que se encontro 
    #punto: la ubicacion central de donde se encuentra esa temperatura. 
    
    
#Buscar la ubicacion de la zona de calor de la seccion 2[13-24]
for x in range(13,25):
    if x == 1:
        print("h")
    elif x == 2:
        print("h")
    elif x == 3:
        print("h")
    #3.	Superior: 6, 9, 12, 15, 18, 21; abajo, izquierda, derecha. (-1, -3, +3)
    #1.	Centro: 5, 8, 11, 14, 17, 20; arriba, abajo, izquierda, derecha. (+1,-1,-3, +3)
    #7.	Inferior: 4, 7, 10, 13, 16, 19; arriba, izquierda, derecha. (+1,-3, +3)
    #2.	Centro-23; arriba, abajo, izquierda, derecha. (+1,-1,-3, +2)
    #4.	Superior-24; abajo, izquierda, derecha. (-1, -3, +2)
    #12.Esquina inferior derecha-22; arriba, izquierda. (+1, -3)
    
    
#Buscar la ubicacion de la zona de calor de la seccion 3[25-32]
for x in range(25,33):
    if x == 1:
        print("h")
    elif x == 2:
        print("h")
    elif x == 3:
        print("h")
    #5.	Superior-26, 28, 30, 32; abajo, izquierda, derecha. (-1, -2, +2)
    #8.	Inferior-25, 27, 29; arriba, izquierda, derecha. (+1, -2, +3)
    #13.Esquina inferior derecha-31; arriba, izquierda. (+1,-2)
    
#Buscar la ubicacion de la zona de calor de la seccion 4[33-36]
for x in range(33,37):
    if x == 1:
        print("h")
    elif x == 2:
        print("h")
    elif x == 3:
        print("h")
    #6.	Lineal: 33, 34, 35; izquierda, derecha. (-1, +1)
    #14.	Esquina lateral derecha: 36; izquierda. (-1)




##==========================================###

#representa un punto de la linea, los datos necesarios seran su ubicacion y la temperatura


''' Método generico para verificar si la temperatura de un punto adyacente esta fuera de rango
index es el indice del punto que se esta evaluando
numLinea es el numero de línea en el que se encuentra el punto que se esta evaluando
refLinea define cual punto adyacente con exactitud será verificado
lineas es el arreglo de  '''
''' def verificarTemperatura(index : int, numLinea : int , refLinea : int , lineas):
    if lineas[numLinea + refLinea].temperatura[index] > 26 or  lineas[numLinea + refLinea].temperatura[index] < 22:
        print("La temperatura de esta linea tambien esta fuera de rango" + str(lineas[numLinea + refLinea].temperatura[index]))
        return lineas[numLinea + refLinea].temperatura[index]
    return 0 '''