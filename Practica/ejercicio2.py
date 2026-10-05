ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil", "Quito"]
conteo = {}  
for ciudad in ciudades:  
    conteo[ciudad] = conteo.get(ciudad, 0) + 1
print(conteo)
mas_repetida = max(conteo, key=conteo.get)
print(mas_repetida)