import lightbulb
import hikari
import time

hoy = time.gmtime()

fechas = lightbulb.Plugin('fechas', 'Funciones para enviar mensaje en ciertas fechas')

def revisarFechas():
    if hoy.tm_yday == 69:
        return 'Hoy es el día 69 del año UwU'
    if hoy.tm_mon == 4 and hoy.tm_mday == 20:
        return 'Feliz 4/20 te desea eliasbot :maple_leaf:'
    if hoy.tm_mon == 12 and hoy.tm_mday == 25:
        return 'Feliz navidad te desea eliasbot :mrs_claus:'
    if hoy.tm_mon == 12 and hoy.tm_mday == 24:
        return 'Feliz nochebuena te desea eliasbot :christmas_tree:'
    if hoy.tm_mon == 11 and hoy.tm_mday == 17:
        return f'Hoy hace {hoy.tm_year - 2019} años cayó prepa 9, feliz aniversario les desea eliasbot :Pogchamp:'
    if hoy.tm_mon == 5 and hoy.tm_mday == 5:
        return 'feliz sinco de mayo'
    if hoy.tm_mon == 1 and hoy.tm_mday == 1:
        return 'Feliz año nuevo les desea eliasbot :)'
    if hoy.tm_mon == 12 and hoy.tm_mday == 31:
        return 'Hoy es el ultimo día del año, eliasbot les agradece por este año'


def load(bot):
    bot.add_plugin(fechas)