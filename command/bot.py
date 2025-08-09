import discord
import yt_dlp
import asyncio
from collections import deque
from discord.utils import get
from discord import app_commands
from datetime import datetime
from discord.ext import commands
from repositories.usuarios_repository import UsuariosRepository
from repositories.preguntas_repository import PreguntasRepository
from repositories.history_repository import HistoryRepository
from models.usuario import Usuario
from services.history_services import HistoryService
from services.preguntas_services import PreguntaService
from services.usuarios_services import UsuarioService

# Configuramos los "intents" para que el bot pueda leer el contenido de los mensajes
intents = discord.Intents.default()
intents.message_content = True

# Creamos el bot con el prefijo de comandos '$' y los intents configurados
bot = commands.Bot(command_prefix="#", intents=intents)

SONG_QUEUE = {}
GUILD_ID = 954872883828650084

usuario_service = UsuarioService(UsuariosRepository())
pregunta_service = PreguntaService(PreguntasRepository())
history_service = HistoryService(HistoryRepository())

@bot.event
async def on_ready():
    test_guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=test_guild)
    
    print(f"Hemos iniciado sesión como {bot.user}")

@bot.command()
async def private(ctx):
    usuario = usuario_service.obtener_por_username(ctx.author.name)
    if not usuario:
        await ctx.send(
            f"No estás registrado. Usa el comando #register para registrarte.")
        return
    await ctx.author.send("Bienvenido usuario aqui te envio la informacion")


@bot.command()
async def clear(ctx, amount: int):
    usuario = usuario_service.obtener_por_username(ctx.author.name)
    if not usuario:
        await ctx.send(
            f"No estás registrado. Usa el comando #register para registrarte.")
        return
    
    if amount <= 0:
        await ctx.send("Por favor, ingresa la cantidad de mensajes que deseas borrar.")
        return
    
    if amount > 50:
        await ctx.send("No puedes borrar más de 50 mensajes a la vez.")
        return
    
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Se eliminaron {len(deleted) - 1} mensajes.")
    await asyncio.sleep(2)
    await ctx.channel.purge(limit=1)
    
@bot.command()
async def register(ctx):
    user, is_created = usuario_service.crear(ctx.author.id, ctx.author.name, ctx.author.display_name, ctx.author.avatar.url)
    if is_created:
        await ctx.send(
            f"¡Bienvenido {user.display_name}! Has sido registrado exitosamente. 🌱"
        )
    else:
        await ctx.send(f"{user.display_name}, ya estás registrado en el sistema. 😊")
        
        
@bot.command()
async def question(ctx):
    usuario = usuario_service.obtener_por_username(ctx.author.name)
    if not usuario:
        await ctx.send(
            f"No estás registrado. Usa el comando #register para registrarte.")
        return

    
    p = pregunta_service.obtener_pregunta_random()
    await ctx.send(f"{usuario.display_name} la pregunta es:\n{p.pregunta}")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        # Espera la respuesta del usuario por 30 segundos
        respuesta_usuario = await bot.wait_for("message", check=check, timeout=30.0)

        if respuesta_usuario.content.lower() == p.respuesta.lower():

            usuario_service.actualizar_coins(usuario, p.ganancia)
            
            print(respuesta_usuario.created_at)
            history_service.insertar(
                usuario.id,
                p.id,
                p.ganancia,
                respuesta_usuario.created_at,
                respuesta_usuario.content,    
            )
            await ctx.send(f"¡Correcto! {usuario.display_name}. ¡Has ganado {p.ganancia} eco-coins 🌟!")
        else:
            usuario_service.actualizar_coins(usuario, p.perdida)

            history_service.insertar(
                usuario.id,
                p.id,
                p.perdida,
                respuesta_usuario.created_at,
                respuesta_usuario.content,
            )
            await ctx.send(
                f"Incorrecto {usuario.display_name}. La respuesta correcta era: {p.respuesta}\nHas perdido {p.perdida} eco-coins 😢"
            )

    except TimeoutError:
        await ctx.send(
            f"Se acabó el tiempo, {usuario.display_name}! La respuesta correcta era: {p.respuesta}"
        )


@bot.command()
async def ranking(ctx):
    usuario = usuario_service.obtener_por_username(ctx.author.name)
    if not usuario:
        await ctx.send(
            f"No estás registrado. Usa el comando #register para registrarte.")
        return
    
    usuarios = usuario_service.obtener_ranking()
    if not usuarios:
        await ctx.send("No hay usuarios registrados.")
        return

    mensaje = "🏆 **Ranking de Usuarios Ecologicos** 🏆\n"
    for i, u in enumerate(usuarios, start=1):
        mensaje += f"{i}. {u.display_name} - {u.coins} eco-coins\n"
    await ctx.send(mensaje)


@bot.command()
async def info(ctx):
    usuario = usuario_service.obtener_por_discord_id(ctx.author.id)
    if usuario:
        await ctx.send(f"{usuario.display_name}, tienes {usuario.coins} eco-coins.")
    else:
        await ctx.send(
            f"No estás registrado. Usa el comando #register para registrarte."
        )


@bot.command()
async def history(ctx):
    usuario = usuario_service.obtener_por_username(ctx.author.name)
    if not usuario:
        await ctx.send(f"No estás registrado. Usa el comando #register para registrarte.")
        return

    history = history_service.obtener_por_usuario(usuario)
    if len(history) == 0:
        await ctx.send("No tienes historial de preguntas.")
        return
    
    mensaje = "Historial de Preguntas:\n"
    for h in history:
        p = pregunta_service.obtener_pregunta(h.id_pregunta)
        fecha = datetime.strptime(str(h.fecha), "%Y-%m-%d %H:%M:%S.%f%z")
        fecha_formateada = fecha.strftime("%d/%m/%Y %H:%M")
        mensaje += f"Pregunta: {p.pregunta}, Respuesta:, {p.respuesta}, Eco-coins: {h.coins}, Fecha: {fecha_formateada}\n"
    await ctx.send(mensaje)


@bot.command(pass_context=True)
async def conectar(ctx):
    usuario = usuario_service.obtener_por_username(ctx.author.name)
    if not usuario:
        await ctx.send(
            f"No estás registrado. Usa el comando #register para registrarte.")
        return
    
    canal = ctx.message.author.voice.channel
    if not canal:
        await ctx.send("No estás conectado a un canal de voz.")
        return
    voz = get(bot.voice_clients,guild=ctx.guild)
    if voz and voz.is_connected():
        await voz.move_to(canal)
    else:
        voz = await canal.connect()
        
        
@bot.command(pass_context=True)
async def desconnect(ctx):
    usuario = usuario_service.obtener_por_username(ctx.author.name)
    if not usuario:
        await ctx.send(
            f"No estás registrado. Usa el comando #register para registrarte.")
        return
    
    voz = get(bot.voice_clients, guild=ctx.guild)
    await voz.disconnect()
    

# --- Función para buscar canciones (YouTube Search) ---
async def search_ytdlp_async(song_query, ydl_options):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(song_query, ydl_options))

def _extract(song_query, ydl_options):
    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        return ydl.extract_info(song_query, download=False)

# --- Función para obtener stream real (reproducible por ffmpeg) ---
def extract_stream(video_url):
    stream_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'extract_flat': False,
    }
    with yt_dlp.YoutubeDL(stream_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return info["url"], info.get("title", "Sin título")

# --- Comando !play ---
@bot.command()
async def play(ctx, *, song_query: str=""):
    usuario = usuario_service.obtener_por_username(ctx.author.name)
    if not usuario:
        await ctx.send(
            f"No estás registrado. Usa el comando #register para registrarte.")
        return
    
    if song_query == "":
        await ctx.send("Tienes que poner el titulo de la cancion.")
        return
    
    if not ctx.author.voice:
        await ctx.send("No estás conectado a un canal de voz.")
        return

    voice_channel = ctx.author.voice.channel
    voice_client = ctx.guild.voice_client

    try:
        if voice_client is None:
            voice_client = await voice_channel.connect()
        elif voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel)
    except Exception as e:
        await ctx.send(f"Error al conectar: {str(e)}")
        return

    yt_dlp_options = {
        "format": 'bestaudio/best',
        "noplaylist": True,
        "quiet": True,
        "extract_flat": False,
    }

    try:
        song_query_search = "ytsearch1:" + song_query
        results = await search_ytdlp_async(song_query_search, yt_dlp_options)
        tracks = results.get("entries", [])

        if not tracks:
            await ctx.send("No se encontraron resultados para la búsqueda.")
            return

        video_url = tracks[0].get("webpage_url")
        audio_url, title = await asyncio.get_running_loop().run_in_executor(None, extract_stream, video_url)

        guild_id = str(ctx.guild.id)
        if SONG_QUEUE.get(guild_id) is None:
            SONG_QUEUE[guild_id] = deque()

        SONG_QUEUE[guild_id].append((audio_url, title))

        if voice_client.is_playing() or voice_client.is_paused():
            await ctx.send(f"🎵 **{title}** ha sido añadido a la cola.")
        else:
            await next_song(voice_client, guild_id, ctx.channel)

    except Exception as e:
        await ctx.send(f"⚠️ Error: {str(e)}")
        print(f"Error en play: {e}")

# --- Reproducir siguiente canción ---
@bot.command()
async def next(ctx):
    usuario = usuario_service.obtener_por_username(ctx.author.name)
    if not usuario:
        await ctx.send(
            f"No estás registrado. Usa el comando #register para registrarte.")
        return
    
    voz = ctx.guild.voice_client
    if not voz or not voz.is_connected():
        await ctx.send("No estoy conectado a un canal de voz.")
        return

    guild_id = str(ctx.guild.id)
    if guild_id in SONG_QUEUE and SONG_QUEUE[guild_id]:
        if voz.is_playing():
            voz.stop()  # ⛔ Esto ya activa el after_play() que llama a next_song()
            await ctx.send("⏭️ Saltando a la siguiente canción...")
        else:
            # Si no está sonando nada, sí puedes llamarla manualmente
            await next_song(voz, guild_id, ctx.channel)
    else:
        await ctx.send("No hay canciones en la cola para reproducir.")


async def next_song(voz, guild_id, channel):
    if SONG_QUEUE[guild_id]:
        audio_source, title = SONG_QUEUE[guild_id].popleft()

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn"
        }
    
        source = discord.FFmpegPCMAudio(audio_source, **ffmpeg_options, executable="C:\\ffmpeg\\bin\\ffmpeg.exe")

        def after_play(error):
            if error:
                print(f"Error al reproducir la canción: {error}")
            future = asyncio.run_coroutine_threadsafe(next_song(voz, guild_id, channel), bot.loop)
            try:
                future.result()
            except Exception as e:
                print(f"Error en after_play: {e}")

        voz.play(source, after=after_play)
        await channel.send(f"🎶 Reproduciendo: **{title}**")

    else:
        await voz.disconnect()
        SONG_QUEUE[guild_id] = deque()

# --- Comando !skip para saltar canción ---
@bot.command()
async def skip(ctx):
    usuario = usuario_service.obtener_por_username(ctx.author.name)
    if not usuario:
        await ctx.send(
            f"No estás registrado. Usa el comando #register para registrarte.")
        return
    
    vc = ctx.guild.voice_client
    if vc and vc.is_playing():
        vc.stop()
        await ctx.send("⏭️ Canción saltada.")
    else:
        await ctx.send("❌ No hay ninguna canción reproduciéndose.")

@bot.command()
async def pause(ctx):
    usuario = usuario_service.obtener_por_username(ctx.author.name)
    if not usuario:
        await ctx.send(f"No estás registrado. Usa el comando #register para registrarte.")
        return
    
    vc = ctx.guild.voice_client
    if vc.is_playing():
        vc.pause()
        await ctx.send("⏸️ Canción pausada.")
    elif vc.is_paused():
        vc.resume()
        await ctx.send("▶️ Reproducción reanudada.")
    else:
        await ctx.send("❌ No hay ninguna canción reproduciéndose o pausada.")

    