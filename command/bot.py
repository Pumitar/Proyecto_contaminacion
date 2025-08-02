import discord
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


@bot.event
async def on_ready():
    print(f"Hemos iniciado sesión como {bot.user}")


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
