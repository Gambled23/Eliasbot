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
    

@bot.listen(hikari.GuildMessageCreateEvent)
async def printConsoleMessage(event):
    if(event.content == 'elias'):
        mensaje = random.choice(respuestas.elias)
        await event.message.respond(f'"{mensaje}" \n-Elias')
    elif(event.content == 'lol' or event.content == 'un lol'):
        mensaje = random.choice(respuestas.lol)
        await event.message.respond(f'{mensaje} \n<@&810955574488465420>')
    elif(event.content == 'que ricas patas'):
        await event.message.respond(f'A ver {event.author.username} :eyes:')
    elif(event.content == 'Las mujeres no sirven para nada'):
        await event.message.respond(f'jajajaja q risa {event.author.username} con tus payasadas eres un naco y estupido')    
    elif(event.content == 'se logro' or event.content == 'se logró'):
        await event.message.respond(f'Chinga tu madre {event.author.username}')
    elif(event.content == 'uwu' or event.content == 'UwU' or event.content == 'UWU'):
        if(event.author.id != 809479840444186654):
            mensaje = random.choice(respuestas.uwu)
            await event.message.respond(mensaje)
    elif (event.content == 'Me quiero matar' or event.content == 'Me voy a matar' or event.content == 'me voy a pegar un tiro' or event.content == 'me voy a suicidar' or event.content == 'voy a matarme'):
        mensaje = random.choice(respuestas.matarse)
        await event.message.respond(mensaje)
    elif(event.content == 'pendejo' or event.content == 'baboso'):
        await event.message.respond('<@567039496533573632> ahi te hablan')

# @bot.listen(hikari.GuildMessageCreateEvent)
# async def printConsoleMessage(event):
#    if(event.author.id == 320649011000246272):
#         await event.message.respond('Cesar envio el mensaje')
#    elif(event.author.id != 809479840444186654):
#         await event.message.respond('Alguien mas envio el mensaje')


# Comandos
@bot.command
@lightbulb.command('insulto', 'Dice un insulto racial!')
@lightbulb.implements(lightbulb.SlashCommand)
async def insultoCDO(ctx):
    await ctx.respond(random.choice(respuestas.insulto))


@bot.command
@lightbulb.command('lol', 'Quieres jugar lol?')
@lightbulb.implements(lightbulb.SlashCommand)
async def lolCDO(ctx):
    mensaje = random.choice(respuestas.lol)
    await ctx.respond(f'{mensaje}" \n<@&810955574488465420>')

#Crashea por alguna razon!!
#@bot.command
#@lightbulb.command('changelog', 'Ver los registros de cambio')
#@lightbulb.implements(lightbulb.SlashCommand)
#async def changelogCDO(ctx):
#    await ctx.respond(respuestas.cambios)

@bot.command
@lightbulb.command('auxilio', 'Solo usalo en una emergencia si necesitas hablar con alguien')
@lightbulb.implements(lightbulb.SlashCommand)
async def auxilioCDO(ctx):
    mensaje = f'<@&315186853986828290> Creo que {ctx.author.username} necesita hablar con alguien, escuchenlo, yo lo haria pero solo soy eliasbot :('
    await ctx.respond(mensaje)

@bot.command
@lightbulb.command('biblia', 'Genera una frase biblica')
@lightbulb.implements(lightbulb.SlashCommand)
async def auxilioCDO(ctx):
    mensaje = random.choice(respuestas.biblia)
    await ctx.respond(mensaje)
bot.run()
