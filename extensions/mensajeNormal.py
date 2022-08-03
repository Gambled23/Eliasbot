import imp
import hikari
import lightbulb
import random
import respuestas
import os

mensajeNormal = lightbulb.Plugin('mensajenormal', 'Responder a un mensaje sin slash o prefijo')

@mensajeNormal.listener(hikari.GuildMessageCreateEvent)
async def printConsoleMessage(event):
    match event.content:
        case 'elias':
            em = hikari.Embed(title="Elias dice:",description= random.choice(respuestas.elias), color=0x007006)
            em.set_thumbnail('https://i.imgur.com/Yddg0yL.jpeg')
            await event.message.respond(em)
        case 'lol'|'un lol':
            mensaje = random.choice(respuestas.lol)
            mensajeFinal = mensaje + '\n<@&810955574488465420>'
        case 'que ricas patas':
            mensajeFinal = 'a ver ' + event.author.username + ' :eyes:'
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
        case 'que bonita estás':
            mensajeFinal = 'ok simp'
        case 'que bonita estas':
            mensajeFinal = 'No le sabes a los acentos ' + event.author.username
        case '#p boys dont cry'|'#p the cure boys dont cry'|'#p boys dont cry the cure':
            mensajeFinal = random.choice(['tas bien bro?', 'bro...', 'booooys doooont cryyyy'])
        case 'un baropapas':
            mensajeFinal = random.choice(['Letsfuckingooooo', 'pensé q nunca lo dirías', 'BAROPAPASALAVERGA'])
        case 'ramiro':
            mensajeFinal = 'que chingue su madre ese puto viejo de mierda a la verga pinche señor inútil le voy a clavar un cuchillo en la puta garganta mientras me tomo su sangre y me masturbo en el agujero que le quedó del navajazo'
        case 'luis':
            mensajeFinal = 'chinga tu madre no me digas luis'
        case 'Roman'|'roman'|'Román'|'román':
            mensajeFinal = 'andele pendeja'
        case 'Eliasbot podemos jugar lol?'|'eliasbot podemos jugar lol?':
            mensajeFinal = random.choice(['sí','no'])
        case 'sex':
            mensajeFinal = random.choice(respuestas.sexo)
        case '69'|'sesenta y nueve':
            mensajeFinal = random.choice(respuestas.seisnueve)
        case '420'|'4:20'|'cuatro veinte':
            mensajeFinal = random.choice(respuestas.cuatroveinte)
        case 'skyrim':
            mensajeFinal = 'puto todd'
        case 'ando bien pedo'|'ando bien pacheco'|'extraño a mi ex'|'ando bien grifo'|'ando bien drogado'|'ando medio pedo':
            mensajeFinal = 'ya duermete wey al chile'
        case "I would say I'm sorry"|'i would say im sorry':
            if (event.author.id != 809479840444186654):
                mensajeFinal = 'If I thought that it would change your mind'
        case 'If I thought that it would change your mind'|'if I thought that it would change your mind':
            if (event.author.id != 809479840444186654):
                mensajeFinal = 'But I know that this time'
        case 'But I know that this time'|'but I know that this time':
            if (event.author.id != 809479840444186654):
                mensajeFinal = 'I have said too much'
        case 'I have said too much'|'i have said too much':
            if (event.author.id != 809479840444186654):
                mensajeFinal = 'Been too unkind'
        case 'Been too unkind'|'been too unkind':
            if (event.author.id != 809479840444186654):
                mensajeFinal = 'I tried to laugh about it'
        case 'I tried to laugh about it'|'i tried to laugh about it':
            if (event.author.id != 809479840444186654):
                mensajeFinal = 'Cover it all up with lies'
        case 'Cover it all up with lies'|'cover it all up with lies':
            if (event.author.id != 809479840444186654):
                mensajeFinal = 'Hiding the tears in my eyes'
        case 'Hiding the tears in my eyes'|'hiding the tears in my eyes':
            if (event.author.id != 809479840444186654):
                mensajeFinal = "Cause boys don't cry"
        case "Cause boys don't cry"|"cause boys don't cry"|"Cause boys dont cry"|"cause boys dont cry":
            if (event.author.id != 809479840444186654):
                mensajeFinal = "Booooooys don't cry"
        case "boys dont cry"|"boys don't cry"|"Boys don't cry"|"Boys dont cry":
            if (event.author.id != 809479840444186654):
                mensajeFinal = "BOOOOOYS DON'T CRYYY"
        case 'Tania' | 'tania':
            mensajeFinal = 'ese nombre está prohibido en este servidor'
        case 'Jazmin' | 'jazmin' | 'Jazmín' | 'jazmín' | 'lizbeth' | 'Lizbeth':
            mensajeFinal = 'si fue césar denle un putaso por pendejo xfa'     
        case 'testing':
            mensajeFinal = 'puto'       

    try:
        await event.message.respond(mensajeFinal)
    except:
        pass

def load(bot):
    bot.add_plugin(mensajeNormal)
