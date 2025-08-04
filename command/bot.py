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

# Configuramos los "intents" para que el bot pueda leer el contenido de los mensajes
intents = discord.Intents.default()
intents.message_content = True

# Creamos el bot con el prefijo de comandos '$' y los intents configurados
bot = commands.Bot(command_prefix="$", intents=intents)

SONG_QUEUE = {}
GUILD_ID = 954872883828650084


@bot.event
async def on_ready():
    test_guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=test_guild)
    
    print(f"Hemos iniciado sesión como {bot.user}")


@bot.command()
async def register(ctx):
    user = Usuario(None, ctx.author.id, ctx.author.name)
    usuarios_repository = UsuariosRepository()

    if usuarios_repository.registrar_usuario(user):
        await ctx.send(
            f"¡Bienvenido {user.username}! Has sido registrado exitosamente. 🌱"
        )
    else:
        await ctx.send(f"{user.username}, ya estás registrado en el sistema. 😊")
        
        
@bot.command()
async def question(ctx):
    username = ctx.author.name
    usuarios_repository = UsuariosRepository()
    usuario = usuarios_repository.get_usuario(username)
    if not usuario:
        await ctx.send(
            f"No estás registrado. Usa el comando $register para registrarte."
        )
        return

    preguntas_repository = PreguntasRepository()
    historial_repository = HistoryRepository()
    opcion = preguntas_repository.obtener_pregunta_ecologica()
    print(opcion)
    await ctx.send(f"{username} la pregunta es:\n{opcion[1]}")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        # Espera la respuesta del usuario por 30 segundos
        respuesta_usuario = await bot.wait_for("message", check=check, timeout=30.0)

        if respuesta_usuario.content.lower() == opcion[2].lower():
            usuario.modificar_coins(opcion[3])
            usuarios_repository.actualizar_coins(usuario)
            print(respuesta_usuario.created_at)
            historial_repository.insert_history(
                usuario.id,
                opcion[0],
                opcion[3],
                respuesta_usuario.created_at,
                respuesta_usuario.content,
            )
            await ctx.send(f"¡Correcto! {username}. ¡Has ganado {opcion[3]} eco-coins 🌟!")
        else:
            usuario.modificar_coins(opcion[4])
            usuarios_repository.actualizar_coins(usuario)
            historial_repository.insert_history(
                usuario.id,
                opcion[0],
                opcion[4],
                respuesta_usuario.created_at,
                respuesta_usuario.content,
            )
            await ctx.send(
                f"Incorrecto {username}. La respuesta correcta era: {opcion[2]}\nHas perdido {opcion[4]} eco-coins 😢"
            )

    except TimeoutError:
        await ctx.send(
            f"Se acabó el tiempo, {username}! La respuesta correcta era: {opcion[2]}"
        )


@bot.command()
async def ranking(ctx):
    usuarios_repository = UsuariosRepository()

    usuarios = usuarios_repository.obtener_ranked_usuarios()
    if not usuarios:
        await ctx.send("No hay usuarios registrados.")
        return

    mensaje = "🏆 **Ranking de Usuarios Ecologicos** 🏆\n"
    for i, u in enumerate(usuarios, start=1):
        mensaje += f"{i}. {u[2]} - {u[3]} eco-coins\n"

    await ctx.send(mensaje)


@bot.command()
async def info(ctx):
    usuarios_repository = UsuariosRepository()
    usuario = usuarios_repository.obtener_informacion_usuario(ctx.author.id)
    print(usuario)
    if usuario:
        await ctx.send(f"{usuario.username}, tienes {usuario.coins} eco-coins.")
    else:
        await ctx.send(
            f"No estás registrado. Usa el comando $register para registrarte."
        )


@bot.command()
async def history(ctx):
    usuarios_repository = UsuariosRepository()
    history_repository = HistoryRepository()
    preguntas_repository = PreguntasRepository()
    
    usuario = usuarios_repository.get_usuario(ctx.author.name)
    if not usuario:
        await ctx.send(f"No estás registrado. Usa el comando $register para registrarte.")
        return

    history = history_repository.get_by_user(usuario)
    if len(history) == 0:
        await ctx.send("No tienes historial de preguntas.")
        return
    
    mensaje = "Historial de Preguntas:\n"
    for h in history:
        pregunta = preguntas_repository.obtener_pregunta(h[2])
        fecha = datetime.strptime(str(h[4]), "%Y-%m-%d %H:%M:%S.%f%z")
        fecha_formateada = fecha.strftime("%d/%m/%Y %H:%M")
        mensaje += f"Pregunta: {pregunta[1]}, Respuesta:, {h[5]}, Eco-coins: {h[3]}, Fecha: {fecha_formateada}\n"
    await ctx.send(mensaje)


@bot.command(pass_context=True)
async def conectar(ctx):
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
async def desconectar(ctx):
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
async def play(ctx, *, song_query: str):
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
    vc = ctx.guild.voice_client
    if vc and vc.is_playing():
        vc.stop()
        await ctx.send("⏭️ Canción saltada.")
    else:
        await ctx.send("❌ No hay ninguna canción reproduciéndose.")

# --- Evento on_ready para saber que el bot está listo ---
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
        

    