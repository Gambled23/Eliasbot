def f(x):
    match x:
        case 'a':
            print('enviaste a')
        case 'b':
            print('enviaste b')
        case 'c'|'j'|'x':
            print('enviaste x, c, j')
        case _:
            print('enviaste una cadena no registrada') #if x is not found
f('b')
f('a')
f('x')
f('j')
f('c')