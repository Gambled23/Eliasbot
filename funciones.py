#Funciones
def calcularPromedio (alumno1, alumno2, alumno3):
    suma = alumno1 + alumno2 + alumno3
    promedio = suma/3
    return promedio

promedio = calcularPromedio(9,8,6)
print("El promedio es: ", promedio)