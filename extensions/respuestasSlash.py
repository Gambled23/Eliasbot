import hikari
import lightbulb
import random
import respuestas

respuestasSlash = lightbulb.Plugin('Respuestas', 'Respuestas usando el slash')

@respuestasSlash.command
@lightbulb.command('insulto', 'Dice un insulto racial!')
@lightbulb.implements(lightbulb.SlashCommand)
async def insultoCDO(ctx):
    await ctx.respond(random.choice(respuestas.insulto))

@respuestasSlash.command
@lightbulb.command('lol', 'Quieres jugar lol?')
@lightbulb.implements(lightbulb.SlashCommand)
async def lolCDO(ctx):
    mensaje = random.choice(respuestas.lol)
    await ctx.respond(f'{mensaje} \n<@&810955574488465420>')

@respuestasSlash.command
@lightbulb.command('auxilio', 'Solo usalo en una emergencia si necesitas hablar con alguien')
@lightbulb.implements(lightbulb.SlashCommand)
async def auxilioCDO(ctx):
    mensaje = f'<@&315186853986828290> Creo que {ctx.author.username} necesita hablar con alguien, escuchenlo, yo lo haria pero solo soy eliasbot :('
    await ctx.respond(mensaje)

@respuestasSlash.command
@lightbulb.command('biblia', 'Genera una frase biblica')
@lightbulb.implements(lightbulb.SlashCommand)
async def auxilioCDO(ctx):
    mensaje = random.choice(respuestas.biblia)
    await ctx.respond(mensaje)

@respuestasSlash.command
@lightbulb.command('donaciones', 'Ayuda a pagar el host del bot donando')
@lightbulb.implements(lightbulb.SlashCommand)
async def donaciones(ctx):
    await ctx.respond('Hostear eliasbot 24/7 cuesta dinero, si quieres apoyar al eliasbot y al capitalismo dame dinero UwU\nhttps://paypal.me/Gambled23')

@respuestasSlash.command
@lightbulb.command('contribuir', 'Obten el repositorio paara contribuir al bot')
@lightbulb.implements(lightbulb.SlashCommand)
async def repositorio(ctx):
    await ctx.respond('Por seguridad el repositorio debe ser privado UwU\nMandame tu correo de github para agregarte como colaborador 👉👈')




def load(bot):
    bot.add_plugin(respuestasSlash)

