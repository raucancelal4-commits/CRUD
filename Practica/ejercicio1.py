ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]
ciudad = set()
Ecuador = []
for x in ciudades:
    if x not in ciudad:
        ciudad.add(x)
        Ecuador.append(x)
print(Ecuador[2])
print(Ecuador)