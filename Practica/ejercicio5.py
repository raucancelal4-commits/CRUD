ventas = [
    ("enero", 1500),
    ("febrero", 1800),
    ("marzo", 1200)
]

total = sum(monto for _mes, monto in ventas)

mejor_mes, mejor_monto = max(ventas, key=lambda venta: venta[1])

print(f"Total: {total}")
print(f"Mejor mes: {mejor_mes} con {mejor_monto}")

for mes, monto in ventas:
    print(f"{mes:<10} {monto}")