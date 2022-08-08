import lightbulb
import hikari
import time

hoy = time.gmtime()

fechas = lightbulb.Plugin('fechas', 'Funciones para enviar mensaje en ciertas fechas')

async def revisarFechas():
    if hoy.tm_yday == 69:
        await fechas.rest.create_message(320650670258520065, f'Hoy es el día 69 del año UwU')
    if hoy.tm_mon == 4 and hoy.tm_mday == 20:
        await fechas.rest.create_message(320650670258520065, f'Feliz 4/20 te desea eliasbot :maple_leaf:')
    if hoy.tm_mon == 12 and hoy.tm_mday == 25:
        await fechas.rest.create_message(320650670258520065, f'Feliz navidad te desea eliasbot :mrs_claus:')
    if hoy.tm_mon == 12 and hoy.tm_mday == 24:
        await fechas.rest.create_message(320650670258520065, f'Feliz nochebuena te desea eliasbot :christmas_tree:')
    if hoy.tm_mon == 11 and hoy.tm_mday == 17:
        await fechas.rest.create_message(320650670258520065, f'Hoy hace {hoy.tm_year - 2019} el gobierno de prepa 9, feliz aniversario les desea eliasbot :Pogchamp:')



def load(bot):
    bot.add_plugin(fechas)