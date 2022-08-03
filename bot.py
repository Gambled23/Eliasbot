import hikari
import lightbulb
import cumpleanos
import time

hoy = time.gmtime()



import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format


bot = lightbulb.BotApp(token='ODA5NDc5ODQwNDQ0MTg2NjU0.YCVs2Q.yODObIjLuocQuQxIGMo75i8CQYM',
                       # La id del server para que el slash command no tarde tanto
                       default_enabled_guilds=(315186853986828290)
                       )
                       
bot.load_extensions_from('./extensions')

@bot.listen(hikari.StartedEvent)
async def botStarted(event):
    print('\n\n')
    cprint(figlet_format('Eliasbot', font='roman'),
       'white', attrs=['bold'])
    cprint(figlet_format('made by: gambled23', font='straight'),
       'yellow')   
    
    #Cada que se inicia el bot revisa si es el cumpleaños de alguien
    cumpleañero = cumpleanos.verificarCumpleaños()
    if cumpleañero != None:
        await bot.rest.create_message(320650670258520065, f'Hoy es el CUM del <@{cumpleañero[3]}>\nFeliz CUM numero {hoy.tm_year - 2003} te desea Eliasbot :birthday: :partying_face:')

bot.run()