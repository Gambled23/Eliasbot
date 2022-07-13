import hikari
import lightbulb
import respuestas
import random

dm = lightbulb.Plugin('dms', 'Cuando el bot recibe dms')

@dm.listener(hikari.MessageCreateEvent)
async def responderDms(event):
    if(event.is_human):
        await event.message.respond(random.choice(respuestas.dm))

def load(bot):
    bot.add_plugin(dm)