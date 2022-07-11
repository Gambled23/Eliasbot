import asyncio
import json
import logging
import random
import re
from datetime import date
from typing import Optional

import hikari
import lavasnek_rs
import lightbulb
import spotipy
from lightbulb.utils import nav, pag
from spotipy.oauth2 import SpotifyClientCredentials
from yarl import URL

from utils.const import URL_REGEX, TIME_REGEX, SPOTCLIENT_ID, SPOTCLIENT_SECRET, LAVALINK_SERVER, LAVALINK_PASSWORD, \
    LAVALINK_PORT, LAVALINK_SSL

music_plugin = lightbulb.Plugin("music", "Music Related commands", include_datastore=True)
music_plugin.add_checks(lightbulb.checks.guild_only)


class LavalinkEventHandler:
    async def track_start(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackStart) -> None:
        logging.info(f"Track started on guild: {event.guild_id}")
        try:
            guild_node = await lavalink.get_guild_node(event.guild_id)
            song = await music_plugin.d.lavalink.decode_track(event.track)
            chanid = guild_node.get_data().get("ChannelID")
            firsttrack = guild_node.get_data().get("First")
            loop_enabled = guild_node.get_data().get("loop")

            if not firsttrack:
                embed = hikari.Embed(title="**Reproduciendo siguiente canción**", description=f"[{song.title}]({song.uri})",
                                     color=0x00FF00)
                embed.add_field(name="Artista", value=song.author, inline=False)
                identifier = song.identifier
                thumb = f"http://img.youtube.com/vi/{identifier}/0.jpg"
                embed.set_thumbnail(thumb)
            elif loop_enabled:
                return
            else:
                embed = hikari.Embed(title="**Reproduciendo ahora**", description=f"[{song.title}]({song.uri})",
                                     color=0x00FF00)
                embed.add_field(name="Artista", value=song.author, inline=False)
                identifier = song.identifier
                thumb = f"http://img.youtube.com/vi/{identifier}/0.jpg"
                embed.set_thumbnail(thumb)

            resp = await music_plugin.bot.rest.create_message(chanid, embed=embed)
            await asyncio.sleep(15)
            await resp.delete()
        except:
            pass

    async def track_finish(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackFinish) -> None:
        guild_node = await lavalink.get_guild_node(event.guild_id)
        try:
            loop_enabled = guild_node.get_data().get("loop")
            if loop_enabled:
                song = await music_plugin.d.lavalink.decode_track(event.track)
                result = await music_plugin.d.lavalink.get_tracks(song.uri)
                await lavalink.play(event.guild_id, result.tracks[0]).queue()
                return
        except AttributeError:
            return

        if not guild_node or not guild_node.now_playing and len(guild_node.queue) == 0:
            if event.guild_id is not None:
                await music_plugin.bot.update_voice_state(event.guild_id, None)
                await music_plugin.d.lavalink.wait_for_connection_info_remove(event.guild_id)
            await music_plugin.d.lavalink.destroy(event.guild_id)
            await music_plugin.d.lavalink.remove_guild_from_loops(event.guild_id)
            await music_plugin.d.lavalink.remove_guild_node(event.guild_id)
            logging.info(f"Track finished on guild: {event.guild_id}")
            try:
                chanid = guild_node.get_data().get("ChannelID")
                await music_plugin.bot.rest.create_message(chanid,
                                                           embed=hikari.Embed(title="**Se terminó la cola de reproducción**",
                                                                              color=0xFFFF00))
            except:
                pass
            return

    async def track_exception(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackException) -> None:
        logging.warning(f"Track exception event happened on guild: {event.guild_id}")

        guild_node = await lavalink.get_guild_node(event.guild_id)
        chanid = guild_node.get_data().get("ChannelID")

        emb = hikari.Embed(title=f"An Exception Occured while trying to play the song.",
                           description=event.exception_message, colour=0xC80000)
        emb.add_field(name="Cause", value=event.exception_cause)
        emb.add_field(name="Track Exception Type", value=event.track_exception_type)
        emb.add_field(name="Exception Severity", value=event.exception_severity)

        await music_plugin.bot.rest.create_message(chanid, embed=emb)

        # If a track was unable to be played, skip it
        skip = await lavalink.skip(event.guild_id)
        node = await lavalink.get_guild_node(event.guild_id)

        if not node:
            return

        if skip and not node.queue and not node.now_playing:
            await lavalink.stop(event.guild_id)


@music_plugin.listener(hikari.ShardReadyEvent)
async def start_lavalink(event: hikari.ShardReadyEvent) -> None:
    builder = (
        lavasnek_rs.LavalinkBuilder(event.my_user.id, "")
            .set_host(LAVALINK_SERVER)
            .set_port(int(LAVALINK_PORT))
            .set_password(LAVALINK_PASSWORD)
            .set_is_ssl(bool(LAVALINK_SSL))
            .set_start_gateway(False)
    )
    lava_client = await builder.build(LavalinkEventHandler())
    music_plugin.d.lavalink = lava_client


@music_plugin.listener(hikari.VoiceStateUpdateEvent)
async def voice_state_update(event: hikari.VoiceStateUpdateEvent) -> None:
    music_plugin.d.lavalink.raw_handle_event_voice_state_update(
        event.state.guild_id,
        event.state.user_id,
        event.state.session_id,
        event.state.channel_id,
    )


# Use an event listener to listen to VC events
@music_plugin.listener(hikari.VoiceServerUpdateEvent)
async def voice_server_update(event: hikari.VoiceServerUpdateEvent) -> None:
    await music_plugin.d.lavalink.raw_handle_event_voice_server_update(event.guild_id, event.endpoint, event.token)


@music_plugin.listener(hikari.VoiceStateUpdateEvent)
async def ensure_voice_empty(event: hikari.VoiceStateUpdateEvent) -> None:
    if event.state.member.is_bot:
        return  # we don't care about bots

    try:
        bot_state = music_plugin.bot.cache.get_voice_state(event.guild_id, music_plugin.bot.application.id)
        if not bot_state:
            return  # if the bot is not in the VC we don't care what's going on

        if event.state.channel_id != bot_state.channel_id or event.old_state.channel_id == bot_state.channel_id:
            return  # if the user is not in the same voice channel as the bot. don't do anything.
    except AttributeError:
        return

    members = music_plugin.bot.cache.get_voice_states_view_for_channel(event.guild_id, event.state.channel_id)
    # Check to see if all humans left the VC
    if not [m for m in members if not members[m].member.is_bot]:
        # do stuff knowing everyone has left the VC
        guild_node = await music_plugin.d.lavalink.get_guild_node(event.guild_id)

        if event.guild_id is not None:
            await music_plugin.bot.update_voice_state(event.guild_id, None)
            await music_plugin.d.lavalink.wait_for_connection_info_remove(event.guild_id)
        await music_plugin.d.lavalink.destroy(event.guild_id)
        await music_plugin.d.lavalink.remove_guild_from_loops(event.guild_id)
        await music_plugin.d.lavalink.remove_guild_node(event.guild_id)

        try:
            chanid = guild_node.get_data().get("ChannelID")
            await music_plugin.bot.rest.create_message(chanid, embed=hikari.Embed(
                title="**Ya que el VC está vacío, me salí para ahorrar recursos**", color=0xFFFF00))
        except:
            pass


async def _join(ctx: lightbulb.Context) -> Optional[hikari.Snowflake]:
    assert ctx.guild_id is not None

    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]

    if not voice_state:
        embed = hikari.Embed(title="**No estás en ningún canal de voz**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None

    channel_id = voice_state[0].channel_id

    await music_plugin.bot.update_voice_state(ctx.guild_id, channel_id, self_deaf=True, self_mute=False)
    connection_info = await music_plugin.d.lavalink.wait_for_full_connection_info_insert(ctx.guild_id)

    await music_plugin.d.lavalink.create_session(connection_info)

    return channel_id


@music_plugin.command()
@lightbulb.command("join", "entra a tu canal de voz", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def join(ctx: lightbulb.Context) -> None:
    channel_id = await _join(ctx)
    if channel_id:
        embed = hikari.Embed(title="**Unido al canal de voz**", colour=ctx.author.accent_color)
        await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.command("leave", "sale del canal de voz", auto_defer=True, aliases=["stop"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def leave(ctx: lightbulb.Context) -> None:
    assert (ctx.get_guild)
    await music_plugin.d.lavalink.destroy(ctx.guild_id)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    node.set_data({"loop": False})
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**No estás en ningun canal de voz**", colour=ctx.author.accent_color)
        await ctx.respond(embed=embed)
        return

    if ctx.guild_id is not None:
        await music_plugin.bot.update_voice_state(ctx.guild_id, None)
        await music_plugin.d.lavalink.wait_for_connection_info_remove(ctx.guild_id)

    await music_plugin.d.lavalink.remove_guild_from_loops(ctx.guild_id)
    await music_plugin.d.lavalink.remove_guild_node(ctx.guild_id)
    embed = hikari.Embed(title="**Musica terminada y salí del canal de voz**", colour=ctx.author.accent_color)
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.option("file", "Archivo mp3 que quieres reproducir (no testeado)", hikari.Attachment, required=False)
@lightbulb.option("query", "Nombre o URL de la canción que quieres reproducir (spotify/youtube)",
                  modifier=lightbulb.OptionModifier.CONSUME_REST, required=False, autocomplete=True)
@lightbulb.command("play", "busca y reproduce una canción(usa una opción solamente)", auto_defer=True,
                   aliases=["p", "pl"], pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def play(ctx: lightbulb.Context, query: str, file: hikari.Attachment) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**No estás en un canal de voz**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return

    if file:
        if file.url.endswith("mp3") or file.url.endswith(".flac"):
            query = file.url
        else:
            embed = hikari.Embed(title="**Solo archivos mp3 y flac son aceptados**", colour=0xC80000)
            await ctx.respond(embed=embed)
            return
    elif not query and not file:
        embed = hikari.Embed(title="**Ingresa la canción a reproducir**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return

    await _join(ctx)

    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    ID = ctx.channel_id
    if not node or not node.now_playing:
        node.set_data({"ChannelID": ID, "First": True})
    else:
        node.set_data({"ChannelID": ID, "First": False})

    if "https://open.spotify.com/playlist/" in query:
        await ctx.respond(
            embed=hikari.Embed(title="Playlists de spotify no compatibles", color=ctx.author.accent_color))
        return

    if "https://open.spotify.com/track" in query:
        sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID, client_secret=SPOTCLIENT_SECRET))
        track_link = f"{query}"
        track_id = track_link.split("/")[-1].split("?")[0]
        track = f"spotify:track:{track_id}"
        spotifytrack = sp.track(track)
        trackname = spotifytrack['name'] + " " + spotifytrack["artists"][0]["name"]
        result = f"ytmsearch:{trackname}"
        query_information = await music_plugin.d.lavalink.get_tracks(result)
        await music_plugin.d.lavalink.play(ctx.guild_id, query_information.tracks[0]).requester(ctx.author.id).queue()
        emb = hikari.Embed(title="Canción añadida a la cola", color=ctx.author.accent_color)
        emb.add_field(name="Titulo",
                      value=f"[{query_information.tracks[0].info.title}]({query_information.tracks[0].info.uri})",
                      inline=False)
        emb.add_field(name="Artista", value=f"{query_information.tracks[0].info.author}", inline=False)
        identifier = query_information.tracks[0].info.identifier
        thumb = f"http://img.youtube.com/vi/{identifier}/0.jpg"
        emb.set_thumbnail(thumb)
        length = divmod(query_information.tracks[0].info.length, 60000)
        emb.add_field(name="Duración", value=f"{int(length[0])}:{round(length[1] / 1000):02}")
        await ctx.respond(embed=emb)
        return

    if not re.match(URL_REGEX, query):
        result = f"ytsearch:{query}"
        query_information = await music_plugin.d.lavalink.get_tracks(result)
    else:
        query_information = await music_plugin.d.lavalink.get_tracks(query)

    if query_information:
        name = query_information.tracks[0].info.title
        identifier = query_information.tracks[0].info.identifier
        uri = query_information.tracks[0].info.uri
        thumb = f"http://img.youtube.com/vi/{identifier}/0.jpg"
        length = divmod(query_information.tracks[0].info.length, 60000)
    else:
        embed = hikari.Embed(title="**No se ha encontrado ningún resultado :'v**",
                             colour=0xC80000)
        await ctx.respond(embed=embed)
        return

    emb = hikari.Embed(title="**Añadida a la cola!**", color=ctx.author.accent_color)
    emb.add_field(name="Nombre", value=f"[{name}]({uri})", inline=False)
    emb.add_field(name="Artista", value=query_information.tracks[0].info.author, inline=False)
    emb.add_field(name="Duración", value=f"{int(length[0])}:{round(length[1] / 1000):02}", inline=False)
    emb.set_thumbnail(thumb)

    try:
        await ctx.respond(embed=emb)
        await music_plugin.d.lavalink.play(ctx.guild_id, query_information.tracks[0]).requester(ctx.author.id).queue()
    except lavasnek_rs.NoSessionPresent as e:
        raise e


@play.autocomplete("query")
async def play_autocomplete(opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction):
    query = await music_plugin.d.lavalink.auto_search_tracks(opt.value)
    return [track.info.title for track in query.tracks[:5]]


@music_plugin.command()
@lightbulb.option("percentage", "0-200%", int, max_value=200, min_value=0, default=100)
@lightbulb.command("volumen", "Cambia el volumen de la musica", auto_defer=True, aliases=["v"], pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def volume(ctx: lightbulb.Context, percentage: int) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**No estás en ningún canal de voz**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**No hay canciones reproduciendose actualmente**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return

    embed = hikari.Embed(title=f"**Ahora el volumen está al {percentage}%**", color=ctx.author.accent_color)

    if isinstance(ctx, lightbulb.PrefixContext):
        if percentage > 1000:
            percentage = 1000

    if percentage > 200:
        embed.add_field("**PELIGRO!**",
                        "**You have gone above and beyond the safe threshold of the volume (200%).** \n*May God have mercy on your ears.\n lol este mensaje sale¿¿ q no se supone q no se puede anyways si alguien ve esto los tqm*")

    await music_plugin.d.lavalink.volume(ctx.guild_id, int(percentage))

    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.option("time", "¿A qué minuto quieres ir? (usa el formato 0:00)", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("adelantar", "Salta a un punto especifico de la canción", auto_defer=True, aliases=["se"], pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def seek(ctx: lightbulb.Context, time) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**No estás en un canal de voz**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**No hay canciones reproduciendose actualmente**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    if not (match := re.match(TIME_REGEX, time)):
        embed = hikari.Embed(title="**Tiempo invalido papu :v**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    if match.group(3):
        secs = (int(match.group(1)) * 60) + (int(match.group(3)))
    else:
        secs = int(match.group(1))
    await music_plugin.d.lavalink.seek_millis(ctx.guild_id, secs * 1000)

    embed = hikari.Embed(title=f"**Saltado a {node.now_playing.track.info.title}.**", colour=ctx.author.accent_color)
    try:
        length = divmod(node.now_playing.track.info.length, 60000)

        embed.add_field(name="Current Position", value=f"{time}/{int(length[0])}:{round(length[1] / 1000):02}")
    except:
        pass
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.command("aleatorio", "Ponle aleatorio a la cola!", aliases=["sf"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def shuffle(ctx: lightbulb.Context) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]

    if not voice_state:
        embed = hikari.Embed(title="**No estás en un canal de voz**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None

    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        embed = hikari.Embed(title="**No hay canciones reproduciendose actualmente**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    if not len(node.queue) > 1:
        embed = hikari.Embed(title="**Solo hay una canción en la cola**", color=0xC80000)
        await ctx.respond(embed=embed)
        return

    queue = node.queue[1:]  # Because Index 0 is currently playing song and we don't wanna shuffle that!
    random.shuffle(queue)  # Randomly shuffling the queue!
    queue.insert(0, node.queue[0])  # Inserting the now playing song back into the queue
    node.queue = queue

    await music_plugin.d.lavalink.set_guild_node(ctx.guild_id, node)

    embed = hikari.Embed(title="🔀 Cola randomizada", color=0xC80000)
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.command("replay", "Replayea la canción actual", auto_defer=True, aliases=["rp"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def replay(ctx: lightbulb.Context) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**No estás en un canal de voz**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**No hay canciones reproduciendose actualmente**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    await music_plugin.d.lavalink.seek_millis(ctx.guild_id, 0000)
    embed = hikari.Embed(title=f"**Replayeando {node.now_playing.track.info.title}.**", colour=ctx.author.accent_color)
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.command("skip", "skipea a la siguiente canción", auto_defer=True, aliases=["sk"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def skip(ctx: lightbulb.Context) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**No estás en ningún canal de voz**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    skip = await music_plugin.d.lavalink.skip(ctx.guild_id)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not skip:
        embed = hikari.Embed(title="**No hay más canciones en la cola**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    else:
        # If the queue is empty, the next track won't start playing (because there isn't any),
        # so we stop the player.
        if not node.queue and not node.now_playing:
            await music_plugin.d.lavalink.stop(ctx.guild_id)
            skipped_track = skip.track.info
            await ctx.respond(embed=hikari.Embed(description=f"**Canción saltada:** {skipped_track.title}"))
        else:
            skipped_track = skip.track.info
            new_track = node.queue[0].track.info
            await ctx.respond(embed=hikari.Embed(
                description=f"**Canción saltada:** {skipped_track.title}\n**Reproduciendo ahora:** {new_track.title}"))


@music_plugin.command()
@lightbulb.command("pausar", "Pausa la canción actual", auto_defer=True, aliases=["ps"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def pause(ctx: lightbulb.Context) -> None:
    assert (ctx.guild_id)
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**No estás en un canal de voz**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**No hay canciones reproduciendose actualmente**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    await music_plugin.d.lavalink.pause(ctx.guild_id)
    embed = hikari.Embed(title=f"**Pausada {node.now_playing.track.info.title}.**", colour=ctx.author.accent_color)
    try:
        length = divmod(node.now_playing.track.info.length, 60000)
        position = divmod(node.now_playing.track.info.position, 60000)
        embed.add_field(name="Tiempo actual",
                        value=f"{int(position[0])}:{round(position[1] / 1000):02}/{int(length[0])}:{round(length[1] / 1000):02}")
    except:
        pass
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.command("continuar", "Continua la canción actual", auto_defer=True, aliases=["unpause", "rs"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def resume(ctx: lightbulb.Context) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**No estás en un canal de voz**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**No hay canciones reproduciendose actualmente**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    await music_plugin.d.lavalink.resume(ctx.guild_id)
    embed = hikari.Embed(title=f"**Continuando: {node.now_playing.track.info.title}.**", colour=ctx.author.accent_color)
    try:
        length = divmod(node.now_playing.track.info.length, 60000)
        position = divmod(node.now_playing.track.info.position, 60000)
        embed.add_field(name="Duration Played",
                        value=f"{int(position[0])}:{round(position[1] / 1000):02}/{int(length[0])}:{round(length[1] / 1000):02}")
    except:
        pass
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.command("reproduciendoahora", "Ver qué se está reproduciendo actualmente.", auto_defer=True, aliases=["np", "playing"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def now_playing(ctx: lightbulb.Context) -> None:
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**No se está reproduciendo ninguna canción**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return

    if node.is_paused:
        status = "**⏸ Pausada**"
    else:
        status = "**▶ Reproduciendo actualmente**"

    embed = hikari.Embed(title=status, color=ctx.author.accent_color)
    embed.add_field(name="Nombre", value=f"[{node.now_playing.track.info.title}]({node.now_playing.track.info.uri})",
                    inline=False)
    embed.add_field(name="Artista", value=node.now_playing.track.info.author, inline=False)
    identifier = node.now_playing.track.info.identifier
    thumb = f"http://img.youtube.com/vi/{identifier}/0.jpg"
    embed.set_thumbnail(thumb)
    try:
        length = divmod(node.now_playing.track.info.length, 60000)
        position = divmod(node.now_playing.track.info.position, 60000)
        embed.add_field(name="Duration Played",
                        value=f"{int(position[0])}:{round(position[1] / 1000):02}/{int(length[0])}:{round(length[1] / 1000):02}")
    except:
        pass
    embed.add_field(name="Volumen", value=f"{node.volume}%")
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.command("cola", "Muestra la cola de reproducción", aliases=["q", "que"], auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def queue(ctx: lightbulb.Context) -> None:
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**No hay canciones reproduciendose actualmente**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None
    if len(node.queue) == 1:
        embed = hikari.Embed(title="**La cola de reproducciones está vacía**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None

    songs = [
        f'[{tq.track.info.title} - {tq.track.info.author}]({tq.track.info.uri}) ({int(divmod(tq.track.info.length, 60000)[0])}:{round(divmod(tq.track.info.length, 60000)[1] / 1000):02})'
        for i, tq in enumerate(node.queue[1:], start=1)]

    lst = pag.EmbedPaginator()

    @lst.embed_factory()
    def build_embed(page_index, page_content):
        emb = hikari.Embed(title=f"Cola de reproducción (Page {page_index})", description=page_content,
                           color=ctx.author.accent_color)
        return emb

    i = 1
    for track in songs:
        lst.add_line(f"**{i}.** {track}")
        i += 1

    navigator = nav.ButtonNavigator(lst.build_pages())
    await navigator.run(ctx)


@music_plugin.command()
@lightbulb.option("index", "Index de la canción a eliminar", int, required=True)
@lightbulb.command("eliminar", "Quita una canción de la cola", auto_defer=True, aliases=["r"], pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def remove(ctx: lightbulb.Context, index) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**No estás en un canal de voz**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        embed = hikari.Embed(title="**TNo hay canciones reproduciendose actualmente**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if index == 0:
        embed = hikari.Embed(title=f"**No puedes quitar una canción que se está reproduciendo actualmente**", color=0xC80000)
        await ctx.respond(embed=embed)
        return
    try:
        queue = node.queue
        song_to_be_removed = queue[index]
    except:
        embed = hikari.Embed(title=f"**Posición incorrecta**", color=0xC80000)
        await ctx.respond(embed=embed)
        return
    try:
        queue.pop(index)
    except:
        pass
    node.queue = queue
    await music_plugin.d.lavalink.set_guild_node(ctx.guild_id, node)
    embed = hikari.Embed(title=f"**Removida {song_to_be_removed.track.info.title}.**", color=ctx.author.accent_color, )
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.option("position", "La posición de la canción en la cola", int, required=True)
@lightbulb.command("skipto", "skipea a una posición de la cola", auto_defer=True, aliases=["skto"],
                   pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def skipto(ctx: lightbulb.Context, position: int) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**No estás en un canal de voz**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        embed = hikari.Embed(title="**No hay canciones reproduciendose actualmente**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    index = position
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if index == 0:
        embed = hikari.Embed(title=f"**No puedes moverte a una canción que se está reproduciendo actualmente**", color=0xC80000)
        await ctx.respond(embed=embed)
        return
    if index == 1:
        embed = hikari.Embed(title=f"**Skipeando a la siguiente canción.**", color=0xC80000)
        await ctx.respond(embed=embed)
        await music_plugin.d.lavalink.skip(ctx.guild_id)
        return
    try:
        queue = node.queue
        song_to_be_skipped = queue[index]
    except:
        embed = hikari.Embed(title=f"**Posicion incorrecta**", color=0xC80000)
        await ctx.respond(embed=embed)
        return
    queue.insert(1, queue[index])
    queue.pop(index)
    queue.pop(index)
    node.queue = queue
    await music_plugin.d.lavalink.set_guild_node(ctx.guild_id, node)
    await music_plugin.d.lavalink.skip(ctx.guild_id)
    embed = hikari.Embed(title=f"**Skipeado a {song_to_be_skipped.track.info.title}.**", color=ctx.author.accent_color)
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.command("loop", "Pone en loop la canción actual", auto_defer=True, aliases=["repeat", "lp"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def loop(ctx: lightbulb.Context) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not voice_state:
        embed = hikari.Embed(title="**No estás en ningún canal de voz**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None

    if not node or not node.now_playing:
        embed = hikari.Embed(title="**No hay canciones reproduciendose actualmente**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    loop_enabled = node.get_data().get("loop")
    if loop_enabled:
        node.set_data({"loop": False})
        embed = hikari.Embed(title="**Loop desactivado**", color=ctx.author.accent_color)
        await ctx.respond(embed=embed)
    else:
        node.set_data({"loop": True})
        embed = hikari.Embed(title="**Loop activado**", color=ctx.author.accent_color)
        await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.option("new_position", "La nueva posición de la canción en la cola", int, required=True)
@lightbulb.option("current_position", "La posición actual de la canción en la cola", int, required=True)
@lightbulb.command("reordenar", "Mueve una canción de posición en la cola", auto_defer=True, aliases=["mv"],
                   pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def move(ctx: lightbulb.Context, current_position, new_position) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**No estás en un canal de voz**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        embed = hikari.Embed(title="**No hay canciones reproduciendose actualmente**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    new_index = new_position
    old_index = current_position
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not len(node.queue) >= 1:
        embed = hikari.Embed(title=f"**Solo hay 1 canción en la cola**", color=0xC80000)
        await ctx.respond(embed=embed)
        return
    queue = node.queue
    song_to_be_moved = queue[old_index]
    try:
        queue.pop(old_index)
        queue.insert(new_index, song_to_be_moved)
    except:
        embed = hikari.Embed(title=f"**Posición incorrecta**", color=0xC80000)
        await ctx.respond(embed=embed)
        return
    node.queue = queue
    await music_plugin.d.lavalink.set_guild_node(ctx.guild_id, node)
    embed = hikari.Embed(title=f"**Movida {song_to_be_moved.track.info.title} a la posición #{new_index}.**",
                         color=ctx.author.accent_color)
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.command("vaciar", "Limpia la cola de reproducción", auto_defer=True, aliases=["clear"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def empty(ctx: lightbulb.Context) -> None:
    assert (ctx.guild_id)
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**No estás en un canal de voz**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**No hay canciones reproduciendose actualmente**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    await music_plugin.d.lavalink.stop(ctx.guild_id)
    await music_plugin.d.lavalink.remove_guild_node(ctx.guild_id)
    await music_plugin.d.lavalink.remove_guild_from_loops(ctx.guild_id)
    await music_plugin.bot.update_voice_state(ctx.guild_id, None)
    await music_plugin.d.lavalink.wait_for_connection_info_remove(ctx.guild_id)
    await _join(ctx)
    embed = hikari.Embed(title="**Cola vaciada**", color=ctx.author.accent_color)
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.command("newreleases", "Ve los ultimos lanzamientos de hoy", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def newreleases(ctx: lightbulb.Context) -> None:
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID, client_secret=SPOTCLIENT_SECRET))
    response = sp.new_releases(limit=21)
    albums = response['albums']
    today = date.today()
    embed = hikari.Embed(title=f"**Nuevos lanzamientos - {today}**", color=ctx.author.accent_color)
    embed.add_field(name="Ultimas canciones", value=f"\n".join(
        [f"**{i}.** {item['name']}" for i, item in enumerate(albums['items'][1:], start=1)]))
    img = response['albums']['items'][1]['images'][0]['url']
    try:
        embed.set_thumbnail(img)
    except:
        pass
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.command("trending", "Ver los tracks que están de moda", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def trending(ctx: lightbulb.Context) -> None:
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID, client_secret=SPOTCLIENT_SECRET))
    playlist_URI = "37i9dQZF1DXcBWIGoYBM5M"
    track_uris = [x["track"]["uri"] for x in sp.playlist_items(playlist_URI)["items"]]
    track = sp.track(track_uris[1])
    today = date.today()
    embed = hikari.Embed(title=f"**Trending Tracks - {today}**", color=ctx.author.accent_color)
    embed.add_field(name="Top 20 tracks del día", value=f"\n".join(
        [f"**{i}.** {track['track']['name']}" for i, track in
         enumerate(sp.playlist_items(playlist_URI, limit=21)["items"][1:], start=1)]))
    img = track['album']['images'][0]['url']
    try:
        embed.set_thumbnail(img)
    except:
        pass
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.option("artist", "Artista de la canción", str, required=True)
@lightbulb.option("title", "Titulo de la canción", str, required=True)
@lightbulb.command("letra", "Letras de la canción", auto_defer=True, aliases=["ly"], pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def lyrics(ctx: lightbulb.Context, artist: str, title: str) -> None:
    url = URL.build(scheme="https", host="api.lyrics.ovh", path=f"/v1/{artist}/{title}")
    async with ctx.bot.d.aio_session.get(url) as resp:
        data = json.loads(await resp.read())

    try:
        ly = data["lyrics"]
    except KeyError:
        ly = data["error"]

    emb = hikari.Embed(title=f"Letra de: {artist} - {title}", description=ly)

    await ctx.respond(embed=emb)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(music_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(music_plugin)