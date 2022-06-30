from ctypes import sizeof
import respuestas
import random
import hikari
import lightbulb


bot = lightbulb.BotApp(token='ODA5NDc5ODQwNDQ0MTg2NjU0.YCVs2Q.yODObIjLuocQuQxIGMo75i8CQYM',
                       # La id del server para que el slash command no tarde tanto
                       default_enabled_guilds=(315186853986828290)
                       )
mensajeFinal = ''
# Eventos
@bot.listen(hikari.StartedEvent)
async def botStarted(event):
    print("Bot has been started")
    

@bot.listen(hikari.GuildMessageCreateEvent)
async def printConsoleMessage(event):
    match event.content:
        case 'elias':
            mensaje = random.choice(respuestas.elias)
            await event.message.respond(f'"{mensaje}" \n-Elias')
        case 'lol'|'un lol':
            mensaje = random.choice(respuestas.lol)
            await event.message.respond(f'{mensaje} \n<@&810955574488465420>')
        case 'que ricas patas':
            await event.message.respond(f'A ver {event.author.username} :eyes:')
        case 'Las mujeres no sirven para nada':
            mensajeFinal = 'jajajaja q risa ' + event.author.username +' con tus payasadas eres un naco y estupido'
        case 'se logro'|'se logró':
            mensajeFinal = 'Chinga tu madre' + event.author.username
        case 'uwu'|'UwU'|'UWU':
            if(event.author.id != 809479840444186654): #Si el autor no fue el bot
                mensajeFinal = random.choice(respuestas.uwu)
        case 'me quiero matar'|'me voy a matar'|'me voy a pegar un tiro'|'ya matenme':
            mensajeFinal = random.choice(respuestas.matarse)
        case 'pendejo'|'baboso':
            mensajeFinal = '<@567039496533573632> ahi te hablan'
        case '5'|'cinco':
            mensajeFinal = 'Por el culo te la hinco'
        case '13'|'trece':
            mensajeFinal = 'Entre más me la mamas más me crece'
        case 'eliasbot podemos jugar lol?':
            mensajeFinal = random.choice(['Sí', 'No', 'Quizás'])
        case 'chinga tu madre'|'ctm'|'chinga tu madre pues':
            mensajeFinal = 'la tuya en vinagre'
        case 'pruebota':
            mensajeFinal = 'Mira soy un test'
    await event.message.respond(mensajeFinal)

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
    await ctx.respond(f'{mensaje} \n<@&810955574488465420>')

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

@bot.command
@lightbulb.command('donaciones', 'Ayuda a pagar el host del bot donando')
@lightbulb.implements(lightbulb.SlashCommand)
async def donaciones(ctx):
    await ctx.respond('Hostear eliasbot 24/7 cuesta dinero, si quieres apoyar al eliasbot y al capitalismo dame dinero UwU\nhttps://paypal.me/Gambled23')

@bot.command
@lightbulb.command('contribuir', 'Obten el repositorio paara contribuir al bot')
@lightbulb.implements(lightbulb.SlashCommand)
async def repositorio(ctx):
    await ctx.respond('Por seguridad el repositorio debe ser privado UwU\nMandame tu correo de github para agregarte como colaborador 👉👈')

@bot.command
@lightbulb.command('volado','Lanza una moneda, cara o cruz')
@lightbulb.implements(lightbulb.SlashCommand)
async def volado(ctx):
    resultado = random.choice([True, False])
    if resultado:
        await ctx.respond('Ha salido cara papu')
    else:
        await ctx.respond('Ha salido cruz uwu')

bot.run()
