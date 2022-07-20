import hikari
import lightbulb
import cumpleanos



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
    cumpleanos.verificarCumpleaños()
    
    
'''
@bot.command
@lightbulb.command('testeo','comando de prueba')
@lightbulb.implements(lightbulb.SlashCommand)
async def testeo(ctx):
    em = hikari.Embed(title="Elias dice:", color=0x32441C)
    em.add_field(
        name=random.choice(respuestas.elias),
        value="-Elias",
        inline=False,
    )
    await ctx.respond(em)
'''

bot.run()