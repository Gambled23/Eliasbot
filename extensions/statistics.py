import hikari
import lightbulb
import psutil
import platform
from datetime import datetime

stats_plugin = lightbulb.Plugin("stats", "Statistics of this bot", include_datastore = True)

stats_plugin.d.counter = datetime.now()

def solveunit(input):
    output = ((input // 1024) // 1024) // 1024
    return int(output)

@stats_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.command("estadisticas", "Estadisticas del bot (nomás pa saber)", auto_defer = True)
@lightbulb.implements(lightbulb.SlashCommand)
async def stats(ctx: lightbulb.Context) -> None:
    """Estadisticas de eliasbot."""
    try:
        mem_usage = "{:.2f} MiB".format(
            __import__("psutil").Process(
            ).memory_full_info().uss / 1024 ** 2
        )
    except AttributeError:
        # OS doesn't support retrieval of USS (probably BSD or Solaris)
        mem_usage = "{:.2f} MiB".format(
            __import__("psutil").Process(
            ).memory_full_info().rss / 1024 ** 2
        )
    freq = psutil.cpu_freq(percpu=False).current
    sysboot = datetime.fromtimestamp(psutil.boot_time()).strftime("%B %d, %Y at %I:%M:%S %p")
    uptime = datetime.now() - stats_plugin.d.counter
    hours, rem = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(rem, 60)
    days, hours = divmod(hours, 24)
    guilds = ctx.bot.cache.get_guilds_view()
    users = ctx.bot.cache.get_users_view()
    channels = ctx.bot.cache.get_guild_channels_view()
    
    if days:
        time = "%s días, %s horas, %s minutos, y %s segundos" % (
            days,
            hours,
            minutes,
            seconds,
        )
    else:
        time = "%s horas, %s minutos, y %s segundos" % (
            hours, minutes, seconds)
    em = hikari.Embed(title="Estado del sistema", color=0x32441C)
    em.add_field(
        name=":desktop: Uso del CPU",
        value=f"{psutil.cpu_percent():.2f}% ({psutil.cpu_count(logical=False)} Nucleos / {psutil.cpu_count(logical=True)} Hilos) ({'{:0.2f}'.format(freq)} MHz) \nload avg: {psutil.getloadavg()}",
        inline=False,
    )
    em.add_field(
        name=":computer: Uso de memoria del sistema",
        value=f"**{psutil.virtual_memory().percent}%** Usado",
        inline=False,
    )
    em.add_field(
        name=":dna: Versión del kernel",
        value=platform.platform(aliased=True, terse=True),
        inline=False,
    )
    em.add_field(
        name=":gear: Versión de librería",
        value=f"hikari {hikari.__version__} + Lightbulb {lightbulb.__version__}",
        inline=False,
    )
    em.add_field(
        name="\U0001F4BE Uso de memoria del BOT",
        value=mem_usage,
        inline=False
    )
    em.add_field(
        name=":minidisc: Uso del disco",
        value=f"Tamaño total: {solveunit(psutil.disk_usage('/').total)} GB \nUsado actualmente: {solveunit(psutil.disk_usage('/').used)} GB",
        inline=False,
    )
    em.add_field(
        name="\U0001F553 Tiempo activo del BOT",
        value=time,
        inline=False
    )
    em.add_field(
        name="⏲️ Ultima hora de iniciado del sistema",
        value=sysboot,
        inline=False
    )
    em.add_field(
        name="🛰️ Servers (Guilds)",
        value=str(len(guilds)),
        inline=False
    )
    em.add_field(
        name="🚩 Canales",
        value=str(len(channels)),
        inline=False
    )
    em.add_field(
        name="👥 Usuarios",
        value=str(len(users)),
        inline=False
    )
    await ctx.respond(em)
    
def load(bot) -> None:
    bot.add_plugin(stats_plugin)

def unload(bot) -> None:
    bot.remove_plugin(stats_plugin)