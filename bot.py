from operator import truediv
import os

import hikari
import lightbulb
import sys
import cumpleanos
import time

hoy = time.gmtime()
from extensions import fechas

from colorama import init
init(strip=not sys.stdout.isatty()) 
from termcolor import cprint 
from pyfiglet import figlet_format


bot = lightbulb.BotApp(
   token='ODA5NDc5ODQwNDQ0MTg2NjU0.G84RmB.pZVRT5HveP1c3KYRQfzPziZ7fIdqWazO9v_dG8', 
   intents = hikari.Intents.ALL,
   )
                       
bot.load_extensions_from('./extensions')

if __name__ == '__main__':
   if os.name != 'nt':
      import uvloop
      uvloop.install()

@bot.listen(hikari.StartedEvent)
async def botStarted(event):
   print('\n\n')
   cprint(figlet_format('Eliasbot', font='roman'),
      'white', attrs=['bold'])
   cprint(figlet_format('made by: gambled23', font='straight'),
      'yellow')
    
   cumpleañero = cumpleanos.verificarCumpleaños() #Cada que se inicia el bot revisa si es el cumpleaños de alguien
   if cumpleañero != None:
      await bot.rest.create_message(320650670258520065, f'Hoy es el CUM del <@{cumpleañero[3]}>\nFeliz CUM numero {hoy.tm_year - 2003} te desea Eliasbot :birthday: :partying_face:')
   msg = fechas.revisarFechas()
   if msg:
      await bot.rest.create_message(320650670258520065, msg)

bot.run()