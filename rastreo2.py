
import os
import re

#Modela el objeto línea y sus atributos necesarios para realizar el rastreo
class linea():
    def __init__(self, nombre, ubicacion, temperatura):
        self.ubicacion = ubicacion  #lista de ubicaciones
        self.temperatura = temperatura #lista de temperaturas

#Verifica si la temperatura de un punto esta fuera de rango
def checkTemperaturaFueraDeRango(temperatura, listapc__):
    if  float(temperatura) > 26.0 or  float(temperatura) < 22.0:
        listapc__.append(temperatura)
        return True
    return False
#Calcula cuantos grados fuera del rango se encentra la zona 
def getGradosFueraDeRango(tp_):
    if tp_ < 22.0 or tp_ > 26.0:
        if tp_ < 22.0 :
            return 22.0 - tp_
        else :
            return tp_ - 26.0  
#Calcula el promedio de los puntos fuera de rango
def getTemperaturaPromedio(listapc):
    suma = 0.0
    for pc in listapc:
        suma = suma + float(pc)
    return suma / float(len(listapc))

#0. Puntos consecutivos: analiza los dos siguientes puntos en la misma linea
# El penultimo y ultimo punto de  la lista ocasiona un nullpointer exception
def caso0(lineas_, listapc_,x_,i_):
    print("x: " + str(x_) + "index" + str(i_))
    if i_ <= (len(lineas_[x_].temperatura)-3): #OJO AQUI REVISAR
        checkTemperaturaFueraDeRango(lineas_[x_].temperatura[i_+1],listapc_)
        checkTemperaturaFueraDeRango(lineas_[x_].temperatura[i_+2], listapc_)  

#1. Centro: 5, 8, 11, 14, 17, 20; arriba, abajo, izquierda, derecha. (+1,-1,-3, +3)
def caso1(lineas_, listapc_, x_, i_):
    checkTemperaturaFueraDeRango(lineas_[x_+1].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_-1].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_-3].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_+3].temperatura[i_], listapc_) 
#2.	Centro-23; arriba, abajo, izquierda, derecha. (+1,-1,-3, +2)
def caso2(lineas_, listapc_, x_, i_):
    checkTemperaturaFueraDeRango(lineas_[x_+1].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_-1].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_-3].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_+2].temperatura[i_], listapc_) 
#3.	Superior: 6, 9, 12, 15, 18, 21; abajo, izquierda, derecha. (-1, -3, +3)
def caso3(lineas_, listapc_, x_, i_):
    checkTemperaturaFueraDeRango(lineas_[x_-1].temperatura[i_],listapc_)
    checkTemperaturaFueraDeRango(lineas_[x_-3].temperatura[i_], listapc_)
    checkTemperaturaFueraDeRango(lineas_[x_+3].temperatura[i_], listapc_)
# 4. Superior-24; abajo, izquierda, derecha. (-1, -3, +2)
def caso4(lineas_, listapc_, x_, i_):
    checkTemperaturaFueraDeRango(lineas_[x_-1].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_-3].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_+2].temperatura[i_], listapc_)  
# 5. Superior-26, 28, 30, 32; abajo, izquierda, derecha. (-1, -2, +2)
def caso5(lineas_, listapc_, x_, i_):
    checkTemperaturaFueraDeRango(lineas_[x_-1].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_-2].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_+2].temperatura[i_], listapc_) 
# 6. Lineal: 33, 34, 35; izquierda, derecha. (-1, +1)
def caso6(lineas_, listapc_, x_, i_):
    checkTemperaturaFueraDeRango(lineas_[x_-1].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_+1].temperatura[i_], listapc_) 
# 7. Inferior: 4, 7, 10, 13, 16, 19; arriba, izquierda, derecha. (+1,-3, +3)
def caso7(lineas_, listapc_, x_, i_):
    checkTemperaturaFueraDeRango(lineas_[x_+1].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_-3].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_+3].temperatura[i_], listapc_) 
#8.	Inferior-25, 27, 29; arriba, izquierda, derecha. (+1, -2, +3)
def caso8(lineas_, listapc_, x_, i_):
    checkTemperaturaFueraDeRango(lineas_[x_+1].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_-2].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_+3].temperatura[i_], listapc_) 
#9.	Lateral izquierdo: 2; arriba, abajo, derecha. (+1, -1, +3)
def caso9(lineas_, listapc_, x_, i_):
    checkTemperaturaFueraDeRango(lineas_[x_+1].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_-1].temperatura[i_], listapc_)   
    checkTemperaturaFueraDeRango(lineas_[x_-3].temperatura[i_], listapc_) 
# 10. Esquina superior izquierda: 3; abajo, derecha. (-1, +3) 
def caso10(lineas_, listapc_, x_, i_):
    checkTemperaturaFueraDeRango(lineas_[x_-1].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_+3].temperatura[i_], listapc_)  
# 11. Esquina inferior izquierda: 1; arriba, derecha. (+1, +3)
def caso11(lineas_, listapc_, x_, i_):
    checkTemperaturaFueraDeRango(lineas_[x_+1].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_+3].temperatura[i_], listapc_) 
# 12. Esquina inferior derecha-22; arriba, izquierda. (+1, -3)
def caso12(lineas_, listapc_, x_, i_):
    checkTemperaturaFueraDeRango(lineas_[x_+1].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_-3].temperatura[i_], listapc_) 
# 13. Esquina inferior derecha-31; arriba, izquierda. (+1,-2)
def caso13(lineas_, listapc_, x_, i_):
    checkTemperaturaFueraDeRango(lineas_[x_+1].temperatura[i_], listapc_) 
    checkTemperaturaFueraDeRango(lineas_[x_-2].temperatura[i_], listapc_) 
# 14. Esquina lateral derecha: 36; izquierda. (-1) 
def caso1(lineas_, listapc_, x_, i_):
    checkTemperaturaFueraDeRango(lineas_[x_-1].temperatura[i_], listapc_) 

def setZTFR(seccion, tp_, x_, i_, lineas_, temperaturaZTFR_, diferenciaZTFR_, ubicacionZTFR_, nlineaZTFR_):
    if getGradosFueraDeRango(tp_) > diferenciaZTFR_[seccion]:
        temperaturaZTFR_[seccion] = tp_
        diferenciaZTFR_[seccion] = getGradosFueraDeRango(tp_)
        ubicacionZTFR_[seccion] = lineas_[x_].ubicacion[i_]
        nlineaZTFR_[seccion] = x_+1
        
#obtiene la ruta en donde estan ubicados los archivos con los resultados de comsol
try:
    ruta = ''
    # ruta = os.path.abspath(ruta)+'/resultados' #Ruta linux
    ruta = os.path.abspath(ruta)+'\\Resultados' #Ruta win
except:
    print('Error al obtener la ruta')    
    
lineas = [] #Lista de lineas
#Leerá los 36 archivos de la carpeta resultados y guardará la informacion necesaria en la lista lineas 
for x in range(1,37):
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
        print('Error al leer el archivo')      
    #Transforma data en una lista de líneas del archivo 
    data = re.split('\n',data)
    #Elimina de la lista las primeras 8 líneas
    for y in range(8):
        data.pop(0)   
    #Obtiene la ubicación y la temperatura y las guarda en su respectiva lista
    for d in data:
        datos = d.split();    
        listaUbicaciones.append(datos[0]) 
        listaTemperaturas.append(datos[1])      
    #Inserta un nuevo objeto linea instanciado con los datos obtenidos en la lista lineas
    lineas.append(linea(x, listaUbicaciones, listaTemperaturas))     

temperaturaZTFR = [0.0,0.0,0.0,0.0] # temperaturaZTFR: temperatura promedio de la zona termica fuera de rango 
diferenciaZTFR = [0.0,0.0,0.0,0.0]
ubicacionZTFR = [0.0,0.0,0.0,0.0]  #Ubicacion a lo largo de la línea de la zona termica fuera de rango
nlineaZTFR = [0,0,0,0] #Numero de línea donde esta ubicada la zona termica fuera de rango

#Buscar la ubicacion de la zona termica fuera de rango de la seccion 1[1-12]
for x in range(36):
    for t in lineas[x].temperatura:
        pc =  False  # pc: punto crítico boolean
        tp = 0 # tp: temperatura promedio
        listapc = [] # pc1, pc2, pc3: punto crítico 1, 2 y 3. (temperatura)
        i = lineas[x].temperatura.index(t)
        #se leen los datos de temperatura de cada punto de la línea en busca de una temperatura fuera de rango
        if checkTemperaturaFueraDeRango(t, listapc) == True:
            pc = True
            listapc.append(t)
            caso0(lineas,listapc,x,i)
            #11.Esquina inferior izquierda: 1; arriba, derecha. (+1, +3)
            if x == 1:
                caso11(lineas, listapc, x, i)
            #10.Esquina superior izquierda: 3; abajo, derecha. (-1, +3)
            elif x == 3:
                caso10(lineas,listapc,x,i)
            elif x == 2:
                caso9(lineas, listapc, x, i)
            #3.	Superior: 6, 9, 12, 15, 18, 21; abajo, izquierda, derecha. (-1, -3, +3)
            elif x == 6 or x == 9 or x == 12 or x == 15 or x == 18 or x == 21:
                caso3(lineas,listapc,x,i)
            #1.	Centro: 5, 8, 11, 14, 17, 20; arriba, abajo, izquierda, derecha. (+1,-1,-3, +3)
            elif  x == 5 or x == 8 or x == 11 or x == 14 or x == 17 or x == 20 :
                caso1(lineas,listapc,x,i)
            #7.	Inferior: 4, 7, 10, 13, 16, 19; arriba, izquierda, derecha. (+1,-3, +3)
            elif  x == 4 or x == 7 or x == 10 or x == 13 or x == 16 or x == 19:
                caso7(lineas, listapc, x,i)
                
        if len(listapc) > 3:       #rEVISAR RAZONES DE PORQUE ACEPTA MAYOR A 2 CUANDO LE PONGO MAYOR O IGUAL A 3
            tp = getTemperaturaPromedio(listapc)     
            if x < 12:
                setZTFR(0,tp, x,i,lineas,temperaturaZTFR,diferenciaZTFR,ubicacionZTFR,nlineaZTFR)
            elif x < 24:
                setZTFR(1,tp, x,i,lineas,temperaturaZTFR,diferenciaZTFR,ubicacionZTFR,nlineaZTFR)
            elif x < 32:
                setZTFR(2,tp, x,i,lineas,temperaturaZTFR,diferenciaZTFR,ubicacionZTFR,nlineaZTFR)
            else:
                setZTFR(3,tp, x,i,lineas,temperaturaZTFR,diferenciaZTFR,ubicacionZTFR,nlineaZTFR)
                    

print("Temperatura promedio: " + str(temperaturaZTFR))
print("Linea: " + str(nlineaZTFR))
print(" Ubicacion central de la zona de termica fuera de rango: " + str(ubicacionZTFR))

    
    
#Buscar la ubicacion de la zona de calor de la seccion 2[13-24]

    #3.	Superior: 6, 9, 12, 15, 18, 21; abajo, izquierda, derecha. (-1, -3, +3)
    #1.	Centro: 5, 8, 11, 14, 17, 20; arriba, abajo, izquierda, derecha. (+1,-1,-3, +3)
    #7.	Inferior: 4, 7, 10, 13, 16, 19; arriba, izquierda, derecha. (+1,-3, +3)
    #2.	Centro-23; arriba, abajo, izquierda, derecha. (+1,-1,-3, +2)
    #4.	Superior-24; abajo, izquierda, derecha. (-1, -3, +2)
    #12.Esquina inferior derecha-22; arriba, izquierda. (+1, -3)
    
    
#Buscar la ubicacion de la zona de calor de la seccion 3[25-32]

    #5.	Superior-26, 28, 30, 32; abajo, izquierda, derecha. (-1, -2, +2)
    #8.	Inferior-25, 27, 29; arriba, izquierda, derecha. (+1, -2, +3)
    #13.Esquina inferior derecha-31; arriba, izquierda. (+1,-2)
    
#Buscar la ubicacion de la zona de calor de la seccion 4[33-36]

    #6.	Lineal: 33, 34, 35; izquierda, derecha. (-1, +1)
    #14.	Esquina lateral derecha: 36; izquierda. (-1)



