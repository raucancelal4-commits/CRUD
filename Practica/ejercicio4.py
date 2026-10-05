clientes = [{"id": 1, "nombre":"Ana"}, {"id": 2, "nombre":"Luis"}]
indice = {t["id"]: t["nombre"] for t in clientes}   
print(indice[2]) 