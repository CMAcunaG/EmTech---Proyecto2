import os  # metodos del Sistema Operativo


def clear():  # Borra la pantalla (clear screen)
    os.system('clear')  #


from Usuarios import Valida_User  # validacion de usuarios
from operator import itemgetter  # metodo para el sorted

#
# Proyecto1
#
from lifestore_file import lifestore_products
from lifestore_file import lifestore_sales
from lifestore_file import lifestore_searches

#
# Diccionario de Datos
#
# lifestore_searches [id, id_product]
# >> como lo interpreto para que sea de utilidad
# 0: --- id, consecutuvo, llave unica
# 1: --- id_producto, numero del producto
#
# lifestore_sales [ id_sale, id_product, score, date, refound ]
# 0: --- id_sale, llave unica, consecutivo
# 1: --- id_product,  numero del producto vendido
# 2: --- score  ¿? como lo interpreto ==>RESEÑA
# 3: --- date, fecha de la venta del producto (dd/mm/aaaa)
# 4: --- refound, es 0 o 1, false o true (devolucion)
# 5: --- >>> ¿? Cuantos productos se vendieron de este id_product
#
#
# lifestore_products [ id_product, name, price, catergory, stock]
# 0: --- id del producto, llave unica numerico entero
# 1: --- nombre del producto, alfanumerico
# 2: --- precio del producto, real
# 3: --- categoria del producto, alfanumerico
# 4: --- existencia del producto, entero
#
# producto_vta = [ [ id_product, nombre,  pcio_vta, cantidad, Importe, Stock, Inversion], Categoria, Reseña ]
# 0: id
# 1: nombre
# 2: precio de venta
# 3: 0 cantidad de vendidos
# 4: Importe de la venta
# 5: Stock articulos existentes
# 6: Inversion del producto
# 7: Visitas (buscados)
# 8: Categoria del producto
# 9: Reseña del Producto obtenido de lifestore_sales[2]

# producto_vta_mes = [ [ id_product, nombre,  ventas_mes...]
# 0: id
# 1: nombre
# 2: Importe de la venta 1
# 3: Importe de la venta 2
# 4: Importe de la venta 3
# 5: Importe de la venta 4
# 6: Importe de la venta 5
# 7: Importe de la venta 6
# 8: Importe de la venta 7
# 9: Importe de la venta 8
#10: Importe de la venta 9
#11: Importe de la venta 10
#12: Importe de la venta 11
#13: Importe de la venta 12
#14: Importe de la anual




clear()  # borramos la pantalla

#
# Validacion de Usuario
#
Usuario = input("Dame el usuario : ")
if Valida_User(Usuario) == False:
    quit(1)

# salida a archivo

#
#
#

producto_vta = []
producto_vta_mes = [] 

kont = 0
Ventas_Totales = float(0)

for items in lifestore_products:
    name = [
        items[0],  # 0 : id
        items[1],  # 1 : nombre
        float(items[2]),  # 2 : precio
        float(0),  # 3 : cantidad vendid
        float(0),  # 4 : importe de venta
        float(items[4]),  # 5 : stock
        float(items[4] * items[2]),  # 6 : inversion
        int(0),  # 7 : numero de busquedas
        items[3],  # 8 : categoria del producto
        int(0)  # 9 : reseña del producto desde las ventas
    ]
    producto_vta.append(name)
    name1 = [
        items[0],  # 0 : id
        items[1],  # 1 : nombre
		float(0),  # 2 : venta del mes 1
		float(0),  # 3 : venta del mes 2
		float(0),  # 4 : venta del mes 3
		float(0),  # 5 : venta del mes 4
		float(0),  # 6 : venta del mes 5
		float(0),  # 7 : venta del mes 6
		float(0),  # 8 : venta del mes 7
		float(0),  # 9 : venta del mes 8
		float(0),  #10 : venta del mes 9
		float(0),  #11 : venta del mes 10
		float(0),  #12 : venta del mes 11
		float(0),  #13 : venta del mes 12
		float(0)   #14 : venta acumuladas
	]
    producto_vta_mes.append(name1)

    for vta in lifestore_sales:
        if vta[1] == name[0]:
			# primero los datos generales de las ventas
            if vta[4] == 1:
                name[3] -= 1
            else:
                name[3] += 1
            pcio = name[2]
            cant = float(name[3])
            stock = float(name[5])
            name[4] = float(pcio * cant)  # importe de ventas
            name[6] = float(pcio * stock)  # importe de la inversion
            name[9] = vta[2] # score rango
			#
			#
			# ahora las ventas mensuales
			#
			# dd/mm/aaaa
            fecha = vta[3]
            mes = fecha[3:5]
            X_mes = int(mes) + 1
            if fecha[6:10] == "2020":
                name1[X_mes] = name1 [X_mes] + float(name[2]) ## las ventas es de una
                name1[14] = name1 [14] + float(name[2]) ## las ventas es de una
# ordenado por Importe
vendidos_orden = sorted(producto_vta, key=itemgetter(4), reverse=True)
Ventas_Totales = (0.00)

print("\013\013Productos vendidos por importe de venta" + "\013\013")

for x in vendidos_orden:
    if x[3] != 0:  # fue vendido ¿?
        #print(x) # toda la lista
        Salida = " {:10,.2f} --> {}"
        print(Salida.format(x[4], x[1]))
        Ventas_Totales += (x[4])

Salida = "\013\013Ventas totales {:10,.2f} \013\013"
print(Salida.format(Ventas_Totales))

valor80 = (Ventas_Totales * 0.80)
Acum_Vtas = (0.0)

Salida = "\013\013Los productos que representan el 80-20 de las ventas es {:12,.2f} \013\013"
print(Salida.format(valor80))
for x in vendidos_orden:
    if Acum_Vtas <= valor80:  # para el reporte
        #print(x)  # toda la lista
        Salida = " {:12,.2f} --> {:15s}"
        print(Salida.format(x[4], x[1]))

        Acum_Vtas += (x[4])

#
# Ahora vienen  los reportes por categoria..., pero de menor a mayor
#
#

Categorias = []
# 0: Categoria
# 1: Ventas
# 2: Inversion

print("\013\013productos vendidos agrupados por categoria " + "\013\013")
for x in producto_vta:
    ok = False
    for y in Categorias:
        if x[8] == y[0]:  # es la misma categoria
            ok = True
            break
    if ok == False:  # no existe en categorias
        parte = [x[8], x[4], float(x[5] * x[2])]
        Categorias.append(parte)

#
# Muestra los productos vendidos de la categoria
#
# ordenado por Categoria
#
categoria_orden = sorted(producto_vta, key=itemgetter(8, 4), reverse=False)

# print(Categorias)
for x in Categorias:
    Vtas_Catego = float(0.00)
    print("\013\013" + x[0])
    for y in categoria_orden:
        if x[0] == y[8]:  # es la misma categoria
            if y[4] > 0.0:
                Salida = " - {:10,.2f} -- {:20s}"
                print(Salida.format(y[4], y[1]))
                Vtas_Catego += y[4]
                x[1] = Vtas_Catego

    Salida = "Las ventas {}  {:10,.2f} \t Representa el: {:6,.2%}"
    print(Salida.format(x[0], Vtas_Catego, (Vtas_Catego / Ventas_Totales)))

Catego_Orden = sorted(Categorias, key=itemgetter(1), reverse=False)

print("\013\013 Catergorias <<<\013\013")
for x in Catego_Orden:
    Salida = '  {:>20s}  Ventas: {:10,.2f} que representa el: {:6,.2%} con una Inversion en stock de: {:10,.2f}'
    print(Salida.format(x[0], x[1], float(x[1] / Ventas_Totales), x[2]))

#
# Reportes por numero de busquedas
#
# actualizamos el numero de busquedas de los productos
#

for items in producto_vta:
    last_vta = len(lifestore_searches)
    for vta in lifestore_searches:
        if vta[1] == items[0]:  # mismo producto
            items[7] += 1  # numero de busquedas

# ordenado por Buscados
buscados_orden = sorted(producto_vta, key=itemgetter(7), reverse=False)
Tot_Buscados = 0
print("\013\013Productos Vendidos por numero de buscados" + "\013\013")
for x in buscados_orden:
    if x[7] != 0:
        #print(x) # todo la lista
        Salida = " {:5,} --> {}"
        print(Salida.format(x[7], x[1]))
        Tot_Buscados += x[7]

print("\013\013Total de Busquedas  " + str(Tot_Buscados) + "\013\013")

valor20 = (Tot_Buscados * 0.20)
Acum_Busca = (0.0)
Acum_Vtas = (0.0)
print("\013\013Los productos que representan el 20-80 de los buscados es " +
      str(valor20) + "\013\013")
for x in buscados_orden:
    if Acum_Busca <= valor20:  # para el reporte
        if x[7] > 0:
            Salida = " {:5,} --> {:10,.2f} -- {:15s}"
            print(Salida.format(x[7], x[4], x[1]))
            Acum_Busca += (x[7])
            Acum_Vtas += (x[4])

print("\013\013Y Representan un Total de Ventas " + str(Acum_Vtas) +
      "\013\013")

#
# Ahora los reportes segun el score (rank) de ventas
# el dato ya esta en la lista de productos_vta, en el campo 9
#
#

score_orden = sorted(producto_vta, key=itemgetter(9,4), reverse=True)

print('\013\013Productos vendidos por "score" \013\013')

count = 1
print("Mejores Score \013")
for x in score_orden:
		#print(x) # toda la lista
		Salida = " {}  --> {:10,.2f} --> {}"
		print(Salida.format(x[9], x[4], x[1]))
		count += 1
		if count > 20:
			break


score_orden = sorted(producto_vta, key=itemgetter(9,4), reverse=False)
count = 1
print("\013\013 Menor Score : \013")
for x in score_orden:
	if x[9] > 0:
		#print(x) # toda la lista
		Salida = " {}  --> {:10,.2f} --> {}"
		print(Salida.format(x[9], x[4], x[1]))
		count += 1
		if count > 20:
			break

#
# Generamos la lista de los NO VENDIDOS
#
sin_ventas = []
Inversion = float(0.00)
for x in producto_vta:
    if x[3] == 0:  # fue vendido ¿?
        sin_ventas.append(x)

sin_ventas  = sorted(sin_ventas, key=itemgetter(6), reverse=True)

print("\013\013Productos sin ventas \013\013")
for x in sin_ventas:
    #print(x) # Toda la lista
	Salida = " {:6,.2f} {:12,.2f}  {}"
	print(Salida.format(x[5], x[6], x[1]))  # solo el nombre del producto
	Inversion += x[6]

Salida = "\013\013Inversion total de productos NO VENDIDOS --> {:12,.2f} \013\013"
print(Salida.format(Inversion))


#
# Reportes de ventas mensuales y anuales
#
mes = 0
meses = []

"""
impresion de los datos en forma individual, para validacion

for x in producto_vta_mes:
	Salida = " {}|{}|{:10,.2f}|{:10,.2f}|{:10,.2f}|{:10,.2f}|{:10,.2f}|{:10,.2f}|{:10,.2f}|{:10,.2f}|{:10,.2f}|{:10,.2f}|{:10,.2f}|{:10,.2f}|{:10,.2f} "
	print (Salida.format (x [0],x [1],x [2],x [3],x [4],x [5],x [6],x [7],x [8],x [9],x [10],x [11],x [12],x [13],x [14] ) )
"""

while mes <12:
	mes += 1
	X_mes = mes + 1
	vtas_mes  = sorted(producto_vta_mes, key=itemgetter(X_mes), reverse=True)
	found = False
	Acum_mes = 0.00
	for x in vtas_mes:
		if x[X_mes]>0:
			found = True
			break
	if found:
		#
		# Ahora si imprime la informacion
		#
		print ("\013 Mes : " +str(mes))
		for x in vtas_mes:
			if x[X_mes]>0:
				Salida = " {:10,.2f} | {} | {} "
				print (Salida.format(x[X_mes], x[0], x[1] ))
				Acum_mes += x[14]
		meses.append([mes,Acum_mes])
		Salida = " Ventas Acumuladas del mes {:10,.2f} "
		print (Salida.format (Acum_mes))
	else:
	    meses.append([mes,0.00])
	


print ("\n")


for x in meses:
	Salida = " Mes {:>3} | {:10,.2f} | {:10,.2f} | {:6.2%} "
	print (Salida.format (x[0], x[1], float (x[1]/12), float (x[1] / Ventas_Totales) ))
