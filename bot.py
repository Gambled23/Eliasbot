import hikari
import lightbulb
import cumpleanos

bot = lightbulb.BotApp(token='ODA5NDc5ODQwNDQ0MTg2NjU0.YCVs2Q.yODObIjLuocQuQxIGMo75i8CQYM',
                       # La id del server para que el slash command no tarde tanto
                       default_enabled_guilds=(315186853986828290)
                       )
                       
bot.load_extensions_from('./extensions')

@bot.listen(hikari.StartedEvent)
async def botStarted(event):
    print("Eliasbot ha iniciado correctamente, bienvenido, Gambled")
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