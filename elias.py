from ctypes import sizeof
from random import random
import hikari
import lightbulb

bot = lightbulb.BotApp(token='ODA5NDc5ODQwNDQ0MTg2NjU0.YCVs2Q.yODObIjLuocQuQxIGMo75i8CQYM',
                       # La id del server para que el slash command no tarde tanto
                       default_enabled_guilds=(315186853986828290)
                       )

# Eventos


@bot.listen(hikari.GuildMessageCreateEvent)
async def printConsoleMessage(event):
    print(event.content)


@bot.listen(hikari.StartedEvent)
async def botStarted(event):
    print("Bot has been started")

# Comandos


@bot.command
# Nombre del comando, descripcion
@lightbulb.command('insulto', 'Dice un insulto racial!')
@lightbulb.implements(lightbulb.SlashCommand)
async def pingCommand(ctx):
    
    insulto = ['negro', 'nigga', 'puta', 'chinga tu madre joto', 'te gusta el arroz con popote', 'veta a la verga', 
        'putas mujeres', 'putos judios', 'putos israelitas', 'putos negros', 'el elias se la come',
        'a cuanto el kilo de verga', 'yo solo quiero amor', 'putos blancos', 'putos africanos', 'putos sodomitas', 
        'putos mancos', 'putos discapacitados', '¿En qué se parecen las mujeres a las baldosas? en que las dos se pisan', 
        '¿En qué se parecen las mujeres a las pelotas? en que a las dos se les pega', 
        '¿Qué hace una mujer fuera de la cocina? Turismo', 
        've a hacerme un sandwich elfa :v', 
        'a la cocina pta :vvv']
    await ctx.respond(random.choice(insulto))
bot.run()
