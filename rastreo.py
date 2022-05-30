import os
import re
#representa un punto de la linea, los datos necesarios seran su ubicacion y la temperatura
class lineaDePuntos():
    def __init__(self,ubicacion, temperatura):
        self.ubicacion = ubicacion
        self.temperatura = temperatura
        
def reporteError(mensaje):
    print(mensaje)   
    
#obtiene la ruta en donde estan ubicados los archivos con los resultados de comsol
try:
    ruta = ''
    # ruta = os.path.abspath(ruta)+'/resultados' #Ruta linux
    ruta = os.path.abspath(ruta)+'\\Datos' #Ruta win
except:
    reporteError('Error en obtencion de ruta')
#abre y lee el archivo de resultados
archivoLinea = 'exportaciondedatos_lineaC1.txt'
try:
    f = open (ruta+'/'+archivoLinea,'r+')
    linea = f.read()
    f.close()
except:
    reporteError('Error al leer el archivo')    
try:
    linea = re.split('\n',linea)
    linea.pop(0)
    linea.pop(0)
    linea.pop(0)
    linea.pop(0)
    linea.pop(0)
    linea.pop(0)
    linea.pop(0)
    linea.pop(0)
except:
    reporteError('Error al limpiar y acomodar la lista')  
listaPuntos = []
for punto in linea:
    try:
        datos = punto.split();    
        listaPuntos.append(lineaDePuntos(float(datos[0]),float(datos[1]))) 
    except:
        reporteError('No se guardo correctamente el conjunto de linea')   
diferenciaT = 0.0
diferencia = 0.0
k = 0
n = 0
#Buscar el punto crítico
try:
    for punto in listaPuntos: 
        if punto.temperatura < 22.0 or punto.temperatura > 26.0:
            if punto.temperatura < 22.0 :
                diferenciaT = 22.0 - punto.temperatura
            else :
                diferenciaT = punto.temperatura - 26.0
                if diferenciaT > diferencia :
                    diferencia = diferenciaT
            k = n
        n = n+1
    print('diferencia: ' + str(diferencia) + ' temperatura: ' + str(listaPuntos[k].temperatura) + ' punto: ' +  str(listaPuntos[k].ubicacion))
except:
    reporteError('Error al buscar el punto crítico')  
