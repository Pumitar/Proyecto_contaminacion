# Importamos las bibliotecas necesarias
import discord
from discord.ext import commands
import os, random, requests
from dotenv import load_dotenv
from repositories.usuarios_repository import UsuariosRepository
from repositories.preguntas_repository import PreguntasRepository


# Creamos la conexión a la base de datos


# Cargamos las variables de entorno
load_dotenv()

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
    
    preguntas_repository = PreguntasRepository()
    opcion = preguntas_repository.obtener_pregunta_ecologica()
    print(opcion)
    await ctx.send(f"{username} la pregunta es:\n{opcion[1]}")
    
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    try:
        # Espera la respuesta del usuario por 30 segundos
        respuesta_usuario = await bot.wait_for('message', check=check, timeout=30.0)
        
        if respuesta_usuario.content.lower() == opcion[2].lower():
            await ctx.send(f"¡Correcto! {username}. ¡Has ganado {opcion[3]} coins 🌟!")
        else:
            await ctx.send(f"Incorrecto {username}. La respuesta correcta era: {opcion[2]}\nHas perdido {opcion[4]} coins 😢")
            
    except TimeoutError:
        await ctx.send(f"Se acabó el tiempo, {username}! La respuesta correcta era: {opcion[2]}")


@bot.command()
async def register(ctx):
    user_id = ctx.author.id
    username = ctx.author.name
    
    usuarios_repository = UsuariosRepository()
    if usuarios_repository.registrar_usuario(user_id, username):
        await ctx.send(f"¡Bienvenido {username}! Has sido registrado exitosamente. 🌱")
    else:
        await ctx.send(f"{username}, ya estás registrado en el sistema. 😊")


@bot.command()
async def top(ctx):
    usuarios_repository = UsuariosRepository()

    usuarios = usuarios_repository.obtener_ranked_usuarios()
    if not usuarios:
        await ctx.send("No hay usuarios registrados.")
        return
    
    mensaje = "🏆 **Ranking de Usuarios ecologicos** 🏆\n"
    for i, u in enumerate(usuarios, start=1):
        mensaje += f"{i}. {u[2]} - {u[3]} coins\n"
    
    await ctx.send(mensaje)
    
    
    
    
    
    
    
    
    
# Obtenemos el token desde las variables de entorno
TOKEN = os.getenv("DISCORD_TOKEN")

# Ejecutamos el bot
bot.run(TOKEN)
