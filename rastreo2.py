
import os
import re

from zmq import STREAM_NOTIFY

#Modela el objeto línea y sus atributos necesarios para realizar el rastreo
class linea():
    def __init__(self, nombre, ubicacion, temperatura):
        self.nombre = nombre #nombre de la línea
        self.ubicacion = ubicacion  #lista de ubicaciones
        self.temperatura = temperatura #lista de temperaturas

def reporteError(mensaje):
    print(mensaje)   
    
#Verifica si la temperatura de un punto cercano esta fuera de rango
def verificarTemperatura(temperatura):
    if  float(temperatura) > 26.0 or  float(temperatura) < 22.0:
        #print("La temperatura de esta linea tambien esta fuera de rango" + str(temperatura))
        return temperatura
    return 0






def caso9(lineas_, listapc_, x_, i_):
    if verificarTemperatura(lineas_[x_+1].temperatura[i_]) != 0:
        listapc_.append(lineas_[x_+1].temperatura[i_])
    if verificarTemperatura(lineas_[x_-1].temperatura[i_]) != 0:
       listapc_.append(lineas_[x_-1].temperatura[i_])
    if verificarTemperatura(lineas_[x_-3].temperatura[i_]) != 0:
        listapc_.append(lineas_[x_-3].temperatura[i_])
    

def caso10(lineas_, listapc_, x_, i_):
    if verificarTemperatura(lineas_[x_-1].temperatura[i_]) != 0:
        listapc_.append(lineas_[x_-1].temperatura[i_])
    if verificarTemperatura(lineas_[x_+3].temperatura[i_]) != 0:
        listapc_.append(lineas_[x_+3].temperatura[i_])   

#Calcula el promedio de los puntos cercanos fuera de rango
def calcularPromedio(listapc):
    suma = 0.0
    for pc in listapc:
        suma = suma + float(pc)
    print("suma : " + str(suma))
    return suma / float(len(listapc)) #para evitar la division entre 0



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


#Leerá los 36 archivos de la carpeta resultados y guardará la informacion necesaria en la lista lineas 
for x in range(1,36):
    listaUbicaciones = [] #lista ubicaciones de cada punto en la línea
    listaTemperaturas = [] #lista temperaturas de cada punto en la línea 
    #print("VALOR DE X " + str(x))
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
    for y in range(8):
    # print(y)
        data.pop(0)
    
    #Obtiene la ubicación y la temperatura y las guarda en su respectiva lista
    for d in data:
        datos = d.split();    
        listaUbicaciones.append(datos[0]) 
        listaTemperaturas.append(datos[1]) 
        
    #Inserta un nuevo objeto linea instanciado con los datos obtenidos en la lista lineas
    lineas.append(linea(x, listaUbicaciones, listaTemperaturas))
        
    
''' for l in lineas:
    print("Lista " + str(l.nombre) + "\n")
    for x in range(len(l.ubicacion)):        
        print(str(l.ubicacion[x]) + "-----" + str(l.temperatura[x]) )  '''
    

tpm = 0 # tpm: temperatura promedio máxima 

punto = 0  #es la ubicacion central de la zona termica fuera de rango
nlinea = 0

#Buscar la ubicacion de la zona de calor de la seccion 1[1-12]
for x in range(0,12):
    mnpc =  0
    #print("lineas[x].temperatura : " + str(x+1) + str(lineas[x].temperatura))
    for t in lineas[x].temperatura:
        i = 0 # k: índice del punto analizado.
        pc =  False  # pc: punto crítico boolean
        p = 0 # tp: temperatura promedio
        npc = 0
        tp = 0
        listapc = [] # pc1, pc2, pc3: punto crítico 1, 2 y 3. (temperatura)
        i = lineas[x].temperatura.index(t)
        #se leen los datos de temperatura de cada punto de la línea en busca de una temperatura fuera de rango
        if verificarTemperatura(t) != 0:
            pc = True
            
            listapc.append(t)
            # Cuando se analice penultimo y ultimo punto de punto de la lista esto podria ocasionar un nullpointer ex
            #Debido a esto se analiza hasta el antepenultimo punto
            if i <= (len(lineas[x].temperatura)-2):
                if verificarTemperatura(lineas[x].temperatura[i+1]) != 0:
                    listapc.append(lineas[x].temperatura[i+1])
                if verificarTemperatura(lineas[x].temperatura[i+2]) != 0:
                    listapc.append(lineas[x].temperatura[i+2]) 
            #11.Esquina inferior izquierda: 1; arriba, derecha. (+1, +3)
            if x == 1:
                if verificarTemperatura(lineas[x+1].temperatura[i]) != 0:
                    listapc.append(lineas[x+1].temperatura[i])
                if verificarTemperatura(lineas[x+3].temperatura[i]) != 0:
                    listapc.append(lineas[x+3].temperatura[i])
            #10.Esquina superior izquierda: 3; abajo, derecha. (-1, +3)
            elif x == 3:
                caso10(lineas,listapc,x,i)
            elif x == 2:
                caso9(lineas, listapc, x, i)
            #3.	Superior: 6, 9, 12, 15, 18, 21; abajo, izquierda, derecha. (-1, -3, +3)
            elif x == 6 or x == 9 or x == 12 or x == 15 or x == 18 or x == 21:
                if verificarTemperatura(lineas[x-1].temperatura[i]) != 0:
                    listapc.append(lineas[x-1].temperatura[i])
                if verificarTemperatura(lineas[x-3].temperatura[i]) != 0:
                    listapc.append(lineas[x-3].temperatura[i])
                # print("Valor de x " + str(x))
                # print("Nombre de la linea " + str(lineas[x+2].nombre))
                # print("valor de i " + str(i))
                if verificarTemperatura(lineas[x+3].temperatura[i]) != 0:
                    listapc.append(lineas[x+3].temperatura[i])
            #1.	Centro: 5, 8, 11, 14, 17, 20; arriba, abajo, izquierda, derecha. (+1,-1,-3, +3)
            elif  x == 5 or x == 8 or x == 11 or x == 14 or x == 17 or x == 20 :
                if verificarTemperatura(lineas[x+1].temperatura[i]) != 0:
                    listapc.append(lineas[x+1].temperatura[i])
                if verificarTemperatura(lineas[x-1].temperatura[i]) != 0:
                    listapc.append(lineas[x-1].temperatura[i])
                if verificarTemperatura(lineas[x-3].temperatura[i]) != 0:
                    listapc.append(lineas[x-3].temperatura[i])
                if verificarTemperatura(lineas[x+3].temperatura[i]) != 0:
                    listapc.append(lineas[x+3].temperatura[i])
            #7.	Inferior: 4, 7, 10, 13, 16, 19; arriba, izquierda, derecha. (+1,-3, +3)
            elif  x == 4 or x == 7 or x == 10 or x == 13 or x == 16 or x == 19:
                if verificarTemperatura(lineas[x+1].temperatura[i]) != 0:
                    listapc.append(lineas[x+1].temperatura[i])
                if verificarTemperatura(lineas[x-3].temperatura[i]) != 0:
                    listapc.append(lineas[x-3].temperatura[i])
                if verificarTemperatura(lineas[x+3].temperatura[i]) != 0:
                    listapc.append(lineas[x+3].temperatura[i])
        
        
        if len(listapc) >= 3:       
            tp = calcularPromedio(listapc)     
            print("TEMPERATURA PROMEDIO :" + str(tp))
            mnpc = npc
            if tpm <= tp:
                punto = lineas[x].ubicacion[i]
                nlinea = x+1
                tpm = tp
        
        print("Linea " + str(nlinea))
        print("npc  " + str(npc))
        print("mnpc " + str(mnpc))
        print("tpm " + str(tpm))
        print("tp " + str(tp))
        pc = False
        listapc.clear()
        i = 0
        npc = 0

print("Temperatura promedio maxima: " + str(tpm))
print("Linea " + str(nlinea))
print(" Ubicacion central de la zona de termica fuera de rango: " + str(punto))

            
    #cuando termine de recorrer todas las lineas de la seccion uno, tendremos dos resultados importantes que son;
    #la tpm: la temperatura promedio maxima que se encontro 
    #punto: la ubicacion central de donde se encuentra esa temperatura. 
    
    
#Buscar la ubicacion de la zona de calor de la seccion 2[13-24]
''' for x in range(13,25):
    if x == 1:
        print("h")
    elif x == 2:
        print("h")
    elif x == 3:
        print("h") '''
    #3.	Superior: 6, 9, 12, 15, 18, 21; abajo, izquierda, derecha. (-1, -3, +3)
    #1.	Centro: 5, 8, 11, 14, 17, 20; arriba, abajo, izquierda, derecha. (+1,-1,-3, +3)
    #7.	Inferior: 4, 7, 10, 13, 16, 19; arriba, izquierda, derecha. (+1,-3, +3)
    #2.	Centro-23; arriba, abajo, izquierda, derecha. (+1,-1,-3, +2)
    #4.	Superior-24; abajo, izquierda, derecha. (-1, -3, +2)
    #12.Esquina inferior derecha-22; arriba, izquierda. (+1, -3)
    
    
#Buscar la ubicacion de la zona de calor de la seccion 3[25-32]
''' for x in range(25,33):
    if x == 1:
        print("h")
    elif x == 2:
        print("h")
        print("h") '''
    #5.	Superior-26, 28, 30, 32; abajo, izquierda, derecha. (-1, -2, +2)
    #8.	Inferior-25, 27, 29; arriba, izquierda, derecha. (+1, -2, +3)
    #13.Esquina inferior derecha-31; arriba, izquierda. (+1,-2)
    
#Buscar la ubicacion de la zona de calor de la seccion 4[33-36]
''' for x in range(33,37):
    if x == 1:
        print("h")
    elif x == 2:
        print("h")
    elif x == 3:
        print("h") '''
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