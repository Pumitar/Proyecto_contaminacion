# Importamos las bibliotecas necesarias
import discord
from discord.ext import commands
import os, random, requests
from dotenv import load_dotenv
import sqlite3  

# Creamos la conexión a la base de datos
conexion = sqlite3.connect("contaminacion.db")
cursorBD = conexion.cursor()

# Cargamos las variables de entorno
load_dotenv()

# Configuramos los "intents" para que el bot pueda leer el contenido de los mensajes
intents = discord.Intents.default()  
intents.message_content = True  

# Creamos el bot con el prefijo de comandos '$' y los intents configurados
bot = commands.Bot(command_prefix="$", intents=intents)


# Evento que se activa cuando el bot se conecta correctamente
def registrar_usuario(id_discord, usuario):
    try:
        cursorBD.execute(
            "INSERT INTO usuarios (id_discord, usuario, coins) VALUES (?, ?, ?)",
            (id_discord, usuario, 0)
        )
        conexion.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def obtener_pregunta_ecologica():
    cursorBD.execute("SELECT * FROM preguntas ORDER BY RANDOM() LIMIT 1")
    return cursorBD.fetchone()


def obtener_ranked_usuarios(limit=10):
    cursorBD.execute("SELECT * FROM usuarios ORDER BY coins DESC LIMIT ?", (limit,))
    return cursorBD.fetchall()
    
    
@bot.event
async def on_ready():
    print(f"Hemos iniciado sesión como {bot.user}")


@bot.command()
async def question(ctx):
    username = ctx.author.name
    opcion = obtener_pregunta_ecologica()
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
    
    if registrar_usuario(user_id, username):
        await ctx.send(f"¡Bienvenido {username}! Has sido registrado exitosamente. 🌱")
    else:
        await ctx.send(f"{username}, ya estás registrado en el sistema. 😊")


@bot.command()
async def top(ctx):
    usuarios = obtener_ranked_usuarios()
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
