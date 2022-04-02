from ctypes import sizeof
import respuestas
import random
import hikari
import lightbulb

bot = lightbulb.BotApp(token='ODA5NDc5ODQwNDQ0MTg2NjU0.YCVs2Q.yODObIjLuocQuQxIGMo75i8CQYM',
                       # La id del server para que el slash command no tarde tanto
                       default_enabled_guilds=(315186853986828290)
                       )

# Eventos
@bot.listen(hikari.StartedEvent)
async def botStarted(event):
    print("Bot has been started")


@bot.listen(hikari.GuildMessageCreateEvent) #Eventos de decir cierta palabra sin regex
async def printConsoleMessage(event):
    if(event.content == 'elias'):
        mensaje = random.choice(respuestas.elias)
        await event.message.respond(f'"{mensaje}" \n-Elias')
    if(event.content == 'lol' or 'un lol'):
        mensaje = random.choice(respuestas.lol)
        await event.message.respond(f'{mensaje}" \n<@&810955574488465420>')
    if(event.author.id == 320649011000246272):
        print("Cesar mando el mensaje")
    else:
        print("Alguien mas mando el mensaje")
# Comandos
@bot.command
@lightbulb.command('insulto', 'Dice un insulto racial!') #Nombre del comando, descripcion
@lightbulb.implements(lightbulb.SlashCommand)
async def pingCommand(ctx):
    await ctx.respond(random.choice(respuestas.insulto))

@bot.command
@lightbulb.command('lol', 'Quieres jugar lol?') #Nombre del comando, descripcion
@lightbulb.implements(lightbulb.SlashCommand)
async def pingCommand(ctx):
    mensaje = random.choice(respuestas.lol)
    await ctx.respond(f'{mensaje}" \n<@&810955574488465420>')

@bot.command
@lightbulb.command('changelog', 'Ver los registros de cambio') #Nombre del comando, descripcion
@lightbulb.implements(lightbulb.SlashCommand)
async def pingCommand(ctx):
    await ctx.respond(respuestas.cambios)

bot.run()
