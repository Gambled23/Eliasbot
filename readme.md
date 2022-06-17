# Eliasbot pitón
## Iniciando el bot
Para iniciar el bot solo se debe de clonar todos los archivos de este repositorio, para hacer cambios solo es necesario hacer el commit al repositorio, el bot se reiniciará automaticamente despues de cada commit.

Si lo que quieres es iniciarlo desde la computadora y no desde el host del bot, debes instalar hikari y lightbulb desde la terminal con las siguientes lineas.
```
pip install -U hikari
```
```
pip install hikari-lightbulb
```
Despues solo debes ejecutar el bot.py con python, y el bot dejará de usar los archivos que tengas tú en la computadora y no los que estén en el repositorio de github.
## Nociones basicas
El bot se basa en 2 archivos principales, bot.py y respuestas.py, la declaracion de comandos y eventos están contenidos en el archivo bot, el archivo respuestas solo son los arrays con las respuestas para los comandos con varias respuestas.

## Creando nuevo comando slash
(Solo se usan comandos slash para que el bot responda más rápido)

Para crear un comando slash debes de seguir la siguiente sintaxis
```py
@bot.command
@lightbulb.command('nombreDelComando', 'descripcionDelComando')
@lightbulb.implements(lightbulb.SlashCommand)
async def nombreFuncion(ctx):
    await ctx.respond(texto/variables)
```
Todos los comandos se deben crear dentro del archivo bot.py.

**El nombreDelComando debe de empezar con letras minusculas**.

El ctx es el contexto en el que el bot responderá, es decir, el canal en el que se usó el comando, si lo que quieres es imprimir en la consola usa el print normal de python.
## Crear nueva respuesta para comando existente
Todas las respuestas se guardan en un array en un archivo py, se pueden ver en el archivo respuestas y puedes agregar las que quieras en un array ya existente o crear un nuevo array, no hace falta volver a incluir el nuevo array al archivo del bot porque ya se importó.
### Extras
No borres lineas no mames lo vas a romper.

Si por algo despues de cambiar algo y subir los cambios a github el bot ya no funciona, puedes volver a una versión anterior con git como el puto que eres, o ejecutar al bot desde la consola para ver los errores que está soltando y arreglar tu puta mierda.

### Documentación extra en:

[Hikari doc](https://www.hikari-py.dev/hikari/index.html)

[Lightbulb doc](https://hikari-lightbulb.readthedocs.io/en/latest/)

[Tutorial en video](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
