import csv # metodos para trabajar con archivo csv
import os  # metodos del Sistema Operativo
import time

def Pause(Tiempo):
	if type(Tiempo) != int:
		time.sleep(5.5)    # Pause 5.5 seconds	
	else:
		time.sleep(Tiempo)


def clear():  # Borra la pantalla (clear screen)
    os.system('clear')  #

def Print_Lista (Lista):
	for salida in Lista:
		print (salida)


from Usuarios import Valida_User  # validacion de usuarios
from operator import itemgetter  # metodo para el sorted

clear()  # borramos la pantalla
"""
#
# Validacion de Usuario
#
Usuario = input("Dame el usuario : ")
if Valida_User(Usuario) == False:
    quit(1)

"""
#
# Diccinario de Datos del archivo (synergy_logistics_database.csv)
#
# 0: registro
# 1: direction (exports, imports)
# 2: origin (ciudad)
# 3: destination
# 4: year
# 5: date (dd/mm/aaaa)
# 6: product NameError
# 7: transport_mode (air, rail, road, sea)
# 8: company_name
# 9: total_value 
#

#
# Creamos la lista de elementos del archivo
#
#
# lista de exportaciones
# lista de importaciones
#
Exports = []
Imports = []
Tot_Exports = 0.0
Tot_Imports = 0.0
Kont = 0
# Abrimos el archivo csv de los datos
with open('synergy_logistics_database.csv', "r" ) as Archivo:
	lineas = csv.reader(Archivo)
	for linea in lineas:
		if Kont == 0: # nos brincamos los encabezados
			Kont +=1
			continue
		posicion, tipo,  origen,  destino,  anio,  fecha,  producto, medio, compania, importe = linea		
		importe = float (linea [9])
		info = [origen,  destino,  anio,  fecha,  producto, medio, compania, importe ]		
		if tipo == "Exports":
			# Son exportaciones (Exports)
			Exports.append(info)
			Tot_Exports += importe
		else:
			# Son importaciones (Imports)
			Imports.append(info)
			Tot_Imports += importe

Salida = "Fueron un total de {:9,} -- {:>15} -- {:20,.2f}  "
print (Salida.format ( len(Exports), "Exportaciones", Tot_Exports ))
print (Salida.format ( len(Imports), "Importaciones", Tot_Imports ))


with open("Exports.csv", "w") as out_file:
    buffer  = csv.writer(out_file, quotechar='"')
    buffer.writerows(Exports)


with open("Imports.csv", "w") as out_file:
    buffer  = csv.writer(out_file, quotechar='"')
    buffer.writerows(Imports)



"""
#
# Comparativo de Años
#
Opción 
1) Rutas de importación y exportación. 
Synergy logistics está considerando la posibilidad 
de enfocar sus esfuerzos en las 10 rutas más demandadas. 
Acorde a los flujos de importación y exportación, 
--> ¿cuáles son esas 10 rutas? 
--> ¿le conviene implementar esa estrategia? 
--> ¿porqué?

"""

#
# Exportaciones por Origen, Destino, Año  e Importe
# Importaciones por Origen, Destino, Año e Importe
#

Exports_OD = [  ]

Imports_OD = [  ]

kont = 0
for linea in Exports:

	Origen = linea[0]
	Destino = linea [1]
	Anio = linea[2]
	Importe = float(linea [7])
	datos = [ Origen, Destino, Anio,  float(Importe) ]
	Found = False
	# Haciendo uso de .index
	pos = 0

	for Resto in Exports_OD:
		if Origen == Resto [0]:
			if Destino == Resto [1]:
				if Anio == Resto [2]:
					importe2 = Resto [3] +   Importe
					Resto [3] = importe2
					Found = True
					break

	# Dado que no existe, entonces lo agregamos a la lista
	if Found != True:
		Exports_OD.append(datos)


#	= sorted(lista, key=itemgetter(posi1, pos2...), reverse=True)

# Ordenamos por Año y luego importes en Descendentes (reverse=True)
Exports_OD = sorted(Exports_OD,key=itemgetter(2,3), reverse=True) 

#Print_Lista (Exports_OD)


with open("Exports_ODa.csv", "w") as out_file:
    buffer  = csv.writer(out_file, quotechar='"')
    buffer.writerows(Exports_OD)


#
# Ahora le toca a las Importaciones
#

kont = 0
for linea in Imports:

	Origen = linea[0]
	Destino = linea [1]
	Anio = linea[2]
	Importe = float(linea [7])
	datos = [ Origen, Destino, Anio,  float(Importe) ]
	Found = False
	for Resto in Imports_OD:
		if Origen == Resto [0]:
			if Destino == Resto [1]:
				if Anio == Resto [2]:
					importe2 = Resto [3] +   Importe
					Resto [3] = importe2
					Found = True
					break

	# Dado que no existe, entonces lo agregamos a la lista
	if Found != True:
		Imports_OD.append(datos)


#	= sorted(lista, key=itemgetter(posi1, pos2...), reverse=True)

Imports_OD = sorted(Imports_OD,key=itemgetter(2,3), reverse=True) 
#Print_Lista (Imports_OD)


with open("Imports_ODa.csv", "w") as out_file:
    buffer  = csv.writer(out_file, quotechar='"')
    buffer.writerows(Imports_OD)


#
# Exportaciones
#
registros = len(Exports_OD) 
kont = 1
i = 0
Max = 10


Corte  = Exports_OD [0][2] # El primer año de la lista
List_Exps_Anio = []
List_Imps_Anio = []

export_anio = 0
import_anio = 0

# Ciclo para calcular las exportaciones de cada Año
for data in Exports_OD:
	if Corte == data [2]:
		export_anio += data [3]
	else:
		info=(Corte,export_anio)
		List_Exps_Anio.append (info)
		export_anio = 0
		Corte = data [2] 
# El ultimo de la List_Exps_Anio
info=(Corte,export_anio)
List_Exps_Anio.append (info)

# Ciclo para calcular las importaciones de cada Año
Corte  = Imports_OD [0][2] # El primer año de la lista
for data in Imports_OD:
	if Corte == data [2]:
		import_anio += data [3]
	else:
		info=(Corte,import_anio)
		List_Imps_Anio.append (info)
		import_anio = 0
		Corte = data [2] 
# El ultimo de la List_Exps_Anio
info=(Corte,import_anio)
List_Imps_Anio.append (info)



Corte  = Exports_OD [0][2] # El primer año de la lista
print ("\n\nEXPORTACIONES POR RUTA POR AÑO")

print ("\n\nMonto de Exportacion por Año\n")

for datos in List_Exps_Anio:
	Salida = "       {:4} valor {:18,.2f} representando {:6.2%}"
	porc = datos[1] / Tot_Exports
	print (Salida.format( datos[0], datos [1], porc ) )




indice = 0

while i < registros:
	if kont == 1:
		Corte = Exports_OD [i][2]
		formato = "\n\n\n----> Rutas para el año  {:>4} {:18,.2f} {:6.2%} \n"
		xx,  Tot_Exp_Anio =List_Exps_Anio[indice]
		porc = Tot_Exp_Anio / Tot_Exports
		print (formato.format(Corte,  Tot_Exp_Anio, porc ) )

	
	if Corte == Exports_OD [i][2]:

		if kont<=Max:
			Salida = "{:>2} ---> De {:>15} a {:<15} para {:4} {:18,.2f} {:6.2%} {:6.2%}"
			porc = Exports_OD [i][3] / Tot_Exports
			porc1 = Exports_OD [i][3] / Tot_Exp_Anio
			print (Salida.format (kont, Exports_OD [i][0][0:15], Exports_OD [i][1][0:15], Exports_OD [i][2], Exports_OD [i][3], porc, porc1 ) )
			kont += 1
			for Resto in Imports_OD:
				if Exports_OD [i][0] == Resto [0]:
					if Exports_OD [i][1] == Resto [1]:
						if Exports_OD [i][2] != Resto [2]:
							Salida = "{:>2}         {:>15}   {:<15} para {:4} {:18,.2f} "
							print (Salida.format (" ", " ", " ", Resto[2] , Resto[3]) )

	else:
		Corte  = Exports_OD [i][2]
		kont = 1
		indice += 1

	i += 1
	continue	


#
# Importaciones
#
registros = len(Imports_OD) 
kont = 1
i = 0
indice = 0

Corte = Imports_OD [0][2] # El primer año de la lista


print ("\n\nIMPORTACIONES POR RUTA POR AÑO")


print ("\n\nMonto de Importacion por Año \n")

for datos in List_Imps_Anio:
	Salida = "       {:4} valor {:18,.2f} representando {:6.2%}"
	porc = datos[1] / Tot_Imports
	print (Salida.format( datos[0], datos [1], porc ) )




while i < registros:
	if kont == 1:
		Corte = Imports_OD [i][2]
		formato = "\n\n\n----> Rutas para el año  {:>4} {:18,.2f} {:6.2%} \n"
		xx,  Tot_Imp_Anio =List_Imps_Anio[indice]
		porc = Tot_Imp_Anio / Tot_Imports
		print (formato.format(Corte,  Tot_Imp_Anio, porc ) )


	
	if Corte == Imports_OD [i][2]:

		if kont<=Max:
			Salida = "{:2} ---> De {:>15} a {:<15} para {:4} {:18,.2f} {:6.2%} {:6.2%} "
			porc = Imports_OD [i][3] / Tot_Imports
			porc1 = Imports_OD [i][3] / Tot_Imp_Anio
			print (Salida.format (kont, Imports_OD [i][0][0:15], Imports_OD [i][1][0:15], Imports_OD [i][2], Imports_OD [i][3], porc, porc1 ) )
			kont += 1
			for Resto in Imports_OD:
				if Imports_OD [i][0] == Resto [0]:
					if Imports_OD [i][1] == Resto [1]:
						if Imports_OD [i][2] != Resto [2]:
							Salida = "{:>2}         {:>15}   {:<15} para {:4} {:18,.2f} "
							print (Salida.format (" ", " ", " ", Resto[2] , Resto[3]) )

	else:
		Corte = Imports_OD [i][2]
		kont = 1
		indice += 1

	i += 1
	continue	

""" 
#
# Comparativo de Medios
#
Opción 2) 
Medio de transporte utilizado. 
¿Cuáles son los 3 medios de transporte más importantes para 
Synergy logistics considerando el valor de las importaciones 
y exportaciones? 
¿Cuál es medio de transporte que podrían reducir?

"""

#
# Ahora nos toca generar las listas y no tan listas para el medio
#

#
# Exportaciones por Origen, Destino, Medio  e Importe
# Importaciones por Origen, Destino, Medio  e Importe
#

Exports_OD = [  ]

Imports_OD = [  ]

kont = 0
for linea in Exports:

	Origen  = linea[0]
	Destino = linea [1]
	Medio   = linea[5] # es la posicion 5, Exports
	Importe = float(linea [7])
	datos = [ Origen, Destino, Medio ,  float(Importe) ]
	Found = False

	pos = 0

	for Resto in Exports_OD:
		if Origen == Resto [0]:
			if Destino == Resto [1]:
				if Medio == Resto [2]:
					importe2 = Resto [3] +   Importe
					Resto [3] = importe2
					Found = True
					break

	# Dado que no existe, entonces lo agregamos a la lista
	if Found != True:
		Exports_OD.append(datos)


#	= sorted(lista, key=itemgetter(posi1, pos2...), reverse=True)


Exports_OD = sorted(sorted(Exports_OD, key = lambda x : x[3], reverse = True), key = lambda x : x[2])  
#Print_Lista (Exports_OD)


with open("Exports_ODb.csv", "w") as out_file:
    buffer  = csv.writer(out_file, quotechar='"')
    buffer.writerows(Exports_OD)


#
# Ahora le toca a las Importaciones
#

kont = 0
for linea in Imports:

	Origen = linea[0]
	Destino = linea [1]
	Medio  = linea[5] # Es la posicion 5 de Imports
	Importe = float(linea [7])
	datos = [ Origen, Destino, Medio,  float(Importe) ]
	Found = False
	for Resto in Imports_OD:
		if Origen == Resto [0]:
			if Destino == Resto [1]:
				if Medio == Resto [2]:
					importe2 = Resto [3] +   Importe
					Resto [3] = importe2
					Found = True
					break

	# Dado que no existe, entonces lo agregamos a la lista
	if Found != True:
		Imports_OD.append(datos)


#	= sorted(lista, key=itemgetter(posi1, pos2...), reverse=True)

Imports_OD = sorted(sorted(Imports_OD, key = lambda x : x[3], reverse = True), key = lambda x : x[2])  #Print_Lista (Imports_OD)


with open("Imports_ODb.csv", "w") as out_file:
    buffer  = csv.writer(out_file, quotechar='"')
    buffer.writerows(Imports_OD)

#
# Exportaciones
#
registros = len(Exports_OD) 
kont = 1
i = 0

List_Exps_Medio = []
List_Imps_Medio = []

export_medio = 0
import_medio = 0
Corte  = Exports_OD [0][2] # El primer medio de la lista


# Ciclo para calcular las exportaciones de cada Ruta
for data in Exports_OD:
	if Corte == data [2]:
		export_medio += data [3]
	else:
		info=(Corte,export_medio)
		List_Exps_Medio.append (info)
		export_medio = data [3]
		Corte = data [2] 
# El ultimo de la List_Exps_Anio
info=(Corte,export_medio)
List_Exps_Medio.append (info)

# Ciclo para calcular las importaciones de cada Ruta
Corte  = Imports_OD [0][2] # El primer año de la lista
for data in Imports_OD:
	if Corte == data [2]:
		import_medio += data [3]
	else:
		info=(Corte,import_medio)
		List_Imps_Medio.append (info)
		import_medio = data [3]
		Corte = data [2] 
# El ultimo de la List_Exps_Anio
info=(Corte,import_medio)
List_Imps_Medio.append (info)


Corte  = Exports_OD [0][2] # El primer año de la lista
indice = 0
Max = 5 # solo los primeros 5

print ("\n\nEXPORTACIONES POR MEDIO DE TRANSPORTE")

print ("\n\nMonto de Exportación por Medio\n")

for datos in List_Exps_Medio:
	Salida = "       {:>8} valor {:18,.2f} representando {:6.2%} "
	porc = datos[1] / Tot_Exports
	print (Salida.format( datos[0], datos [1], porc ) )


while i < registros:
		
	if kont == 1:
		Corte = Exports_OD [i][2]
		formato = "\n\n\n----> Rutas detalladas para el medio  {:>4} {:18,.2f} \n"
		xx,  Tot_Exp_Medio =List_Exps_Medio[indice]
		print (formato.format(Corte,  Tot_Exp_Medio ) )

	
	if Corte  == Exports_OD [i][2]:

		if kont<=Max:
			Salida = "{:>2} ---> De {:>15} a {:<15} por {:10} {:18,.2f} {:6.2%} {:6.2%}"

			porc = Exports_OD [i][3] / Tot_Exports
			porc1 = Exports_OD [i][3] / Tot_Exp_Medio
			print (Salida.format (kont, Exports_OD [i][0][0:15], Exports_OD [i][1][0:15], Exports_OD [i][2], Exports_OD [i][3], porc, porc1 ) )
			kont += 1
	else:
		Corte = Exports_OD [i][2]
		kont = 1
		indice += 1


	i += 1
	continue	


#
# Importaciones
#
registros = len(Imports_OD) 
kont = 1
i = 0


Corte  = Imports_OD [0][2] # El primer año de la lista
indice = 0
print ("\n\nIMPORTACIONES POR MEDIO DE TRANSPORTE")

print ("\n\nMonto de Importación por Medio\n")

for datos in List_Imps_Medio:
	Salida = "       {:>8} valor {:18,.2f} representando {:6.2%}"
	porc = datos[1] / Tot_Imports
	print (Salida.format( datos[0], datos [1], porc ) )



while i < registros:
	if kont == 1:
		Corte = Imports_OD [i][2]
		formato = "\n\n\n----> Rutas detalladas para el medio  {:>4} {:18,.2f} \n"
		xx,  Tot_Imp_Medio =List_Imps_Medio[indice]
		print (formato.format(Corte,  Tot_Imp_Medio ) )

	
	if Corte == Imports_OD [i][2]:

		if kont<=Max:
			Salida = "{:>2} ---> De {:>15} a {:<15} por {:10} {:18,.2f} {:6.2%} {:6.2%}"
			porc = Imports_OD [i][3] / Tot_Imports
			porc1 = Imports_OD [i][3] / Tot_Imp_Medio
			print (Salida.format (kont, Imports_OD [i][0][0:15], Imports_OD [i][1][0:15], Imports_OD [i][2], Imports_OD [i][3], porc, porc1 ) )
			kont += 1

	else:
		Corte = Imports_OD [i][2]
		kont = 1
		indice += 1

	i += 1
	continue	


"""
Opción 3) 
Valor total de importaciones y exportaciones. 
Si Synergy Logistics quisiera enfocarse en los países 
que le generan el 80% del valor de las exportaciones e 
importaciones 
¿en qué grupo de países debería enfocar sus esfuerzos?

"""

#
# Primeo Destinos de Exportaciones y Origes de Importaciones
#

Exports_OD1 = [  ]
Imports_OD1 = [  ]

Exports_OD = [  ] # Solo los Destinos
Imports_OD = [  ] # Solo los Origenes



# SOLO  Destino para reporte
kont = 0
for linea in Exports:

	Origen  = linea[0]
	Destino = linea [1]
	Importe = float(linea [7])
	datos = [ Origen, Destino, float(Importe) ]
	Found = False
	pos = 0

	for Resto in Exports_OD:
		#if Origen == Resto [0]:
			if Destino == Resto [1]:
				importe2 = Resto [2] +   Importe
				Resto [2] = importe2
				Found = True
				break

	# Dado que no existe, entonces lo agregamos a la lista
	if Found != True:
		Exports_OD.append(datos)


# Origen y Destino
for linea in Exports:

	Origen  = linea[0]
	Destino = linea [1]
	Importe = float(linea [7])
	datos = [ Origen, Destino, float(Importe) ]
	Found = False
	pos = 0

	for Resto in Exports_OD1:
		if Origen == Resto [0]:
			if Destino == Resto [1]:
				importe2 = Resto [2] +   Importe
				Resto [2] = importe2
				Found = True
				break

	# Dado que no existe, entonces lo agregamos a la lista
	if Found != True:
		Exports_OD1.append(datos)


#	= sorted(lista, key=itemgetter(posi1, pos2...), reverse=True)

# Ordenamos importes en Descendentes (reverse=True)
Exports_OD = sorted(Exports_OD,key=itemgetter(2), reverse=True) 

#Print_Lista (Exports_OD)


with open("Exports_ODc.csv", "w") as out_file:
    buffer  = csv.writer(out_file, quotechar='"')
    buffer.writerows(Exports_OD)

with open("Exports_OD1.csv", "w") as out_file:
    buffer  = csv.writer(out_file, quotechar='"')
    buffer.writerows(Exports_OD1)



#
# Ahora le toca a las Importaciones
#

kont = 0
for linea in Imports:

	Origen = linea[0]
	Destino = linea [1]
	Importe = float(linea [7])
	datos = [ Origen, Destino, float(Importe) ]
	Found = False
	for Resto in Imports_OD:
		if Origen == Resto [0]:
			#if Destino == Resto [1]:
				importe2 = Resto [2] +   Importe
				Resto [2] = importe2
				Found = True
				break

	# Dado que no existe, entonces lo agregamos a la lista
	if Found != True:
		Imports_OD.append(datos)

for linea in Imports:

	Origen = linea[0]
	Destino = linea [1]
	Importe = float(linea [7])
	datos = [ Origen, Destino, float(Importe) ]
	Found = False
	for Resto in Imports_OD1:
		if Origen == Resto [0]:
			if Destino == Resto [1]:
				importe2 = Resto [2] +   Importe
				Resto [2] = importe2
				Found = True
				break

	# Dado que no existe, entonces lo agregamos a la lista
	if Found != True:
		Imports_OD1.append(datos)


#	= sorted(lista, key=itemgetter(posi1, pos2...), reverse=True)

Imports_OD = sorted(Imports_OD,key=itemgetter(2), reverse=True) 
#Print_Lista (Imports_OD)


with open("Imports_ODc.csv", "w") as out_file:
    buffer  = csv.writer(out_file, quotechar='"')
    buffer.writerows(Imports_OD)

with open("Imports_OD1.csv", "w") as out_file:
    buffer  = csv.writer(out_file, quotechar='"')
    buffer.writerows(Imports_OD1)


#
# Exportaciones
#

kont = 1
Tope = 0.0 

print ("\n\nEXPORTACIONES POR IMPORTE  {:18,.2f} y el 80%  {:18,.2f} \n".format (Tot_Exports , (Tot_Exports * 0.80) ))
print (     " Relacion por Destinos\n")

#
# Mostramos el resuen de Exportaciones
#
kont = 1
Tope = 0.00

print (     " Resumen por Destinos\n")
for linea in Exports_OD:
	Salida = "{:>3} ---> {:<15} {:18,.2f}  {:6.2%}"
	porc = linea [2] / Tot_Exports			
	print (Salida.format (kont, linea[1][0:15], linea[2], porc   ) )
	Tope += linea [2]		
	if Tope > (Tot_Exports * 0.80):
		break
	
	kont +=1

kont = 1
Tope = 0.00

print (     "\n Detalle  por Destinos\n")
for linea in Exports_OD:
	Salida = "{:>3} ---> Hacia {:<15} {:18,.2f}  {:6.2%}"
	porc = linea [2] / Tot_Exports			
	print (Salida.format (kont, linea[1][0:15], linea[2], porc   ) )
	Destino = linea[1]

	
	for datos in Exports_OD1:
		xx, yy, zz = datos
		Salida = "         desde {:<15} {:18,.2f} "
		if yy == Destino:
			print (Salida.format (xx[0:15], zz ) )		

	Tope += linea [2]		
	if Tope > (Tot_Exports * 0.80):
		break
	
	kont +=1



#
# Importaciones
#
kont = 1
Tope = 0.0 

print ("\n\nIMPORTACIONES POR IMPORTE  {:18,.2f} y el 80%  {:18,.2f} \n".format (Tot_Imports , (Tot_Imports * 0.80) ))
print (     "  Relacion por Origen \n")
kont = 1
Tope = 0.00
print (     "  Resumen por Origen\n")
for linea in Imports_OD:
	Salida = "{:>3} ---> {:<15} {:18,.2f}  {:6.2%}"
	porc = linea [2] / Tot_Imports			
	print (Salida.format (kont, linea[0], linea[2], porc   ) )
	Origen  = linea[0]
	Tope += linea [2]
	if Tope > (Tot_Imports * 0.80):
		break
	
	kont +=1

kont = 1
Tope = 0.00

print (     "\n Detalle  por Origen\n")
for linea in Imports_OD:
	Salida = "{:>3} ---> Desde {:<15} {:18,.2f}  {:6.2%}"
	porc = linea [2] / Tot_Imports			
	print (Salida.format (kont, linea[0], linea[2], porc   ) )
	Origen  = linea[0]
	Tope += linea [2]

	for datos in Imports_OD1:
		xx, yy, zz = datos
		Salida = "         hacia {:<15} {:18,.2f} "
		if xx == Origen:
			print (Salida.format (yy[0:15], zz ) )		

	

	if Tope > (Tot_Imports * 0.80):
		break
	
	kont +=1


#
# Segundo, INVERTIDO Orignes  de Exportaciones y Destinos de Importaciones
#


Exports_OD = [  ] # Solo los Destinos
Imports_OD = [  ] # Solo los Origenes


kont = 0
# SOLO  Origen  para reporte
kont = 0
for linea in Exports:

	Origen  = linea[0]
	Destino = linea [1]
	Importe = float(linea [7])
	datos = [ Origen, Destino, float(Importe) ]
	Found = False
	pos = 0


	for Resto in Exports_OD:
		if Origen == Resto [0]:
			#if Destino == Resto [1]:
				importe2 = Resto [2] +   Importe
				Resto [2] = importe2
				Found = True
				break

	# Dado que no existe, entonces lo agregamos a la lista
	if Found != True:
		Exports_OD.append(datos)


#	= sorted(lista, key=itemgetter(posi1, pos2...), reverse=True)

# Ordenamos importes en Descendentes (reverse=True)
Exports_OD = sorted(Exports_OD,key=itemgetter(2), reverse=True) 

#Print_Lista (Exports_OD)


with open("Exports_ODd.csv", "w") as out_file:
    buffer  = csv.writer(out_file, quotechar='"')
    buffer.writerows(Exports_OD)


#
# Ahora le toca a las Importaciones
#

kont = 0
for linea in Imports:

	Origen = linea[0]
	Destino = linea [1]
	Importe = float(linea [7])
	datos = [ Origen, Destino, float(Importe) ]
	Found = False
	for Resto in Imports_OD:
		#if Origen == Resto [0]:
			if Destino == Resto [1]:
				importe2 = Resto [2] +   Importe
				Resto [2] = importe2
				Found = True
				break

	# Dado que no existe, entonces lo agregamos a la lista
	if Found != True:
		Imports_OD.append(datos)
	# Dado que no existe, entonces lo agregamos a la lista


#	= sorted(lista, key=itemgetter(posi1, pos2...), reverse=True)

Imports_OD = sorted(Imports_OD,key=itemgetter(2), reverse=True) 
#Print_Lista (Imports_OD)


with open("Imports_ODd.csv", "w") as out_file:
    buffer  = csv.writer(out_file, quotechar='"')
    buffer.writerows(Imports_OD)


#
# Exportaciones
#

kont = 1
Tope = 0.0 

print ("\n\nEXPORTACIONES POR IMPORTE  {:18,.2f} y el 80%  {:18,.2f} \n".format (Tot_Exports , (Tot_Exports * 0.80) ))
print (     " Relacion por Origen\n")
print (     " Resumen por Origen\n")
for linea in Exports_OD:
	Salida = "{:>3} ---> {:<15} {:18,.2f}  {:6.2%}"
	porc = linea [2] / Tot_Exports			
	print (Salida.format (kont, linea[1][0:15], linea[2], porc   ) )
	Tope += linea [2]		
	if Tope > (Tot_Exports * 0.80):
		break
	
	kont +=1

kont = 1
Tope = 0.00

print (     "\n Detalle  por Origen\n")

for linea in Exports_OD:
	Salida = "{:>3} ---> Dede {:<15}  {:18,.2f}  {:6.2%}"
	porc = linea [2] / Tot_Exports			
	print (Salida.format (kont, linea[0][0:15], linea[2], porc   ) )
	Origen = linea[0]
	Tope += linea [2]	
	
	for datos in Exports_OD1:
		xx, yy, zz = datos
		Salida = "         hacia {:<15} {:18,.2f} "
		if xx == Origen:
			print (Salida.format (yy[0:15], zz ) )		

	
	if Tope > (Tot_Exports * 0.80):
		break
	
	kont +=1



#
# Importaciones
#
kont = 1
Tope = 0.0 

print ("\n\nIMPORTACIONES POR IMPORTE  {:18,.2f} y el 80%  {:18,.2f} \n".format (Tot_Imports , (Tot_Imports * 0.80) ))
print (     " Relacion por Destino\n")

print (     " Resumen  por Destino\n")
for linea in Imports_OD:
	Salida = "{:>3} ---> {:<15} {:18,.2f}  {:6.2%}"
	porc = linea [2] / Tot_Imports			
	print (Salida.format (kont, linea[1][0:15], linea[2], porc   ) )
	Destino  = linea[1]
	Tope += linea [2]
	if Tope > (Tot_Imports * 0.80):
		break
	kont +=1

kont = 1
Tope = 0.0 

print (     "\n Detalle  por Destino\n")
for linea in Imports_OD:
	Salida = "{:>3} ---> Hacia {:<15} {:18,.2f}  {:6.2%}"
	porc = linea [2] / Tot_Imports			
	print (Salida.format (kont, linea[1][0:15], linea[2], porc   ) )
	Destino  = linea[1]
	Tope += linea [2]

	for datos in Imports_OD1:
		xx, yy, zz = datos
		Salida = "         desde {:<15} {:18,.2f} "
		if yy == Destino:
			print (Salida.format (xx[0:15], zz ) )		

	

	if Tope > (Tot_Imports * 0.80):
		break
	
	kont +=1




Operaciones = [ ]
Num_Exp=0
Num_Imp=0
Monto_exp=0
Monto_imp=0
#
# 0: Origen
# 1: Destino
# 2: Total  de Exportaciones e Importaciones
# 3: Monto  de Exportaciones e Importaciones
# 4: Numero de Exportaciones
# 5: Monto  de Exportaciones
# 6: Numero de Importaciones
# 7: Monto  de Importaciones
#
# SOLO PARA EL 2020!
#Primero las exportaciones 
#origen, destino, destino1 num_exp, monto_exp, num_imp, Monto_imp, num_oper, Monto_Total
#
#Luego las importaciones
#DESTINO, ORIGEN, destino1, num_exp, monto_exp, num_imp, Monto_imp, num_oper, Monto_Total
#
for linea  in Exports:
	if linea [2] != "2020":
		continue

	Origen = linea[0]
	Destino = linea [1]
	Importe = float(linea [7])
	Found = False
	Datos = [ Origen, Destino, 1, Importe, 1, Importe, 0, 0.0]
	# buscamos a ver si ya existe en Operaciones
	#
	for Buffer in Operaciones:
		if Origen == Buffer[0]:
			if Destino == Buffer [1]:
				#ya existe, aumentamos los valores
				Buffer [2] +=1
				Buffer [3] += Importe
				Buffer [4] +=1
				Buffer [5] += Importe
				Found = True
				break # solo debe haber uno

	# Dado que no existe, entonces lo agregamos a la lista
	if Found != True:
		Operaciones.append(Datos)


for linea  in Imports:
	if linea [2] != "2020":
		continue

	Origen = linea [1]
	Destino = linea[0] # Dado que es importacion


	Importe = float(linea [7])
	Found = False
	Datos = [ Origen, Destino, 1, Importe, 0, 0.00, 1, Importe]

	# buscamos a ver si ya existe en Operaciones
	#
	for Buffer in Operaciones:
		if Origen == Buffer[0]:
			if Destino == Buffer [1]:
				#ya existe, aumentamos los valores
				
				Buffer [2] +=1
				Buffer [3] += Importe
				Buffer [6] +=1
				Buffer [7] += Importe
				Found = True
				break # solo debe haber uno

	if Found != True:
 		Operaciones.append(Datos)

Operaciones =  sorted(Operaciones,key=itemgetter(3), reverse=True) 

NO_Envios = [ ]
#
# 0: Origen
# 1: Destino
#
# En base a Operaciones  
# origen, destino
#
#
for linea  in Operaciones:
	Origen = linea[0]
	Destino = linea [1]
	Found = False

	# buscamos a ver si ya existe en NO_Envios
	#
	for Buffer in Operaciones:
		if Destino  == Buffer[0]: # Destino esta como Origen 
			Found = True
			break # solo debe haber uno

	# Dado que no existe, entonces lo agregamos a la lista
	if Found == False:
		Datos = [ "", Destino]
		for Buffer in NO_Envios:
			if Buffer [1] == Destino:
				Found = True
				break
		if Found == False: # No Existes en NO_Envios
			NO_Envios.append(Datos)
	


for linea  in Operaciones:
	Origen = linea[0]
	Destino = linea [1]
	Found = False

	# buscamos a ver si ya existe en NO_Envios
	#
	for Buffer in Operaciones:
		if Origen == Buffer[1]: #  Origen como Destin o
			Found = True
			break # solo debe haber uno

	# Dado que no existe, entonces lo agregamos a la lista
	# Dado que no existe, entonces lo agregamos a la lista
	if Found == False:
		Datos = [ Origen, ""]
		for Buffer in NO_Envios:
			if Buffer [0] == Origen:
				Found = True
				break
		if Found == False: # No Existes en NO_Envios
			NO_Envios.append(Datos)
		

print ("\n\nOPERACIONES DE ENVIOS Y RECEPCIONES PARA EL 2020\n\n")

print ("                                      Total de Operaciones       Total de Envios         Total de Recepciones")
print ("       Origen     --    Destino     #Oper       Monto        #Oper       Monto        #Oper       Monto       ")
print ("   ...............--............... ..... .................. ..... .................. ..... ..................")
for datos in Operaciones:
	if datos[4] != 0 and datos[6] != 0:
		Salida = "   {:>15}--{:<15} {:5,} {:18,.2f} {:5,} {:18,.2f} {:5,} {:18,.2f}"
		print (Salida.format( datos[0][0:15], datos[1][0:15], datos[2], datos[3], datos[4], datos[5], datos[6], datos[7]  ) )
print ("\n\n")		
for datos in Operaciones:
	if datos[4] != 0 and datos[6] != 0:
		# nada a imorimir	
		Salida = "   {:>15}--{:<15} {:5,} {:18,.2f} {:5,} {:18,.2f} {:5,} {:18,.2f}"		
	else:
		Salida = "   {:>15}--{:<15} {:5,} {:18,.2f} {:5,} {:18,.2f} {:5,} {:18,.2f}"
		print (Salida.format( datos[0][0:15], datos[1][0:15], datos[2], datos[3], datos[4], datos[5], datos[6], datos[7]  ) )

print ("\n\nPAISES SIN OPERACIONES DE ENVIO/RECEPCION PARA EL 2020\n\n")

print ("\n\nPaises como Destinos sin Envios \n")
for datos in NO_Envios:
	if  datos[0] == "":  # Es una Pais SOLO Destino
		print (" ---> " + datos[1] ) 

print ("\n\nPaises como Origen sin Destino \n")
for datos in NO_Envios:
	if  datos[1] == "":  # Es una Pais SOLO Destino
		print (" ---> " + datos[0] ) 



with open("Operaciones.csv", "w") as out_file:
    buffer  = csv.writer(out_file, quotechar='"')
    buffer.writerows(Operaciones)


with open("Sin_Destino-Origen.csv", "w") as out_file:
    buffer  = csv.writer(out_file, quotechar='"')
    buffer.writerows(NO_Envios)


