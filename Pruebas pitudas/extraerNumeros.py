from itertools import count


txt = "pinche pablo t 49 12 15 13 quiero muc2ho"
numeros = [int(s) for s in txt.split() if s.isdigit()]
print(numeros)
suma = 0
for e in numeros:
    suma = suma + e
print(suma)