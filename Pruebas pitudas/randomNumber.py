from ast import While
import random

porcentajes = 0
for i in range(30):
    num = random.randint(1,4)
    print(num)
    if num == 4:
        porcentajes += 1
print(f'El 4 ha salido un {(porcentajes*100)/30}%')