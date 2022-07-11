import lightbulb
import random
import uwuMode

utilidades = lightbulb.Plugin('Utilidaddes', 'Comandos utiles o curiosos')


@utilidades.command
@lightbulb.command('volado','Lanza una moneda, cara o cruz')
@lightbulb.implements(lightbulb.SlashCommand)
async def volado(ctx):
    resultado = random.choice([True, False])
    if resultado:
        await ctx.respond('Ha salido cara papu')
    else:
        await ctx.respond('Ha salido cruz uwu')

@utilidades.command
@lightbulb.option('frase', 'frase a uwuificar')
@lightbulb.command('uwuify','uwuifica una frase')
@lightbulb.implements(lightbulb.SlashCommand)
async def uwuify(ctx):
    await ctx.respond(uwuMode.generateUwU(ctx.options.frase))


def load(bot):
    bot.add_plugin(utilidades)