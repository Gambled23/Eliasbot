import time

hoy = time.gmtime()

cumpleaños = [
    ['pablo', 14, 2, 315185398714204160],
    ['ricardo', 25, 3, 320647538220728321],
    ['victor', 30, 3, 320696604162260993],
    ['alan', 29, 4, 404515319084875789],
    ['christian', 24, 5, 671162712541233184],
    ['elias', 2, 8, 567039496533573632],
    ['massimo', 29, 8, 401203604087898113],
    ['roman', 28, 9, 802291630685552730],
    ['cesar', 16, 12, 320649011000246272]]

def verificarCumpleaños():
    for x in cumpleaños:
        if x[1] == hoy.tm_mday and x[2] == hoy.tm_mon:
            print(x)
            return x
        else:
            print('Hoy no es cumpleaños de', x[0])