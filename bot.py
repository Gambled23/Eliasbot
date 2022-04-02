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
@bot.listen(hikari.GuildMessageCreateEvent)
async def printConsoleMessage(event):
    if(event.content == 'elias'):
        await event.message.respond(random.choice(respuestas.elias))

@bot.listen(hikari.StartedEvent)
async def botStarted(event):
    print("Bot has been started")


# Comandos
@bot.command
@lightbulb.command('insulto', 'Dice un insulto racial!') #Nombre del comando, descripcion
@lightbulb.implements(lightbulb.SlashCommand)
async def pingCommand(ctx):
    await ctx.respond(random.choice(respuestas.insulto))
bot.run()
