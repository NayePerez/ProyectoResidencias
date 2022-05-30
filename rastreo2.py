
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
for x in range(1,37):
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
    
    data.pop(0)
    data.pop(0)
    data.pop(0)
    data.pop(0)
    data.pop(0)
    data.pop(0)
    data.pop(0)
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

# def compararPunto(index, referencia)
# #Buscar la ubicacion de la zona de calor de la seccion 1[1-12]
# for x in range(1,13):
#     print(x)

#Buscar la ubicacion de la zona de calor de la seccion 2[13-24]

#Buscar la ubicacion de la zona de calor de la seccion 3[25-32]

#Buscar la ubicacion de la zona de calor de la seccion 4[33-36]



##==========================================###

#representa un punto de la linea, los datos necesarios seran su ubicacion y la temperatura


