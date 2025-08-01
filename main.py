import os
from command.bot import bot
from dotenv import load_dotenv

# Cargamos las variables de entorno
load_dotenv()

# Obtenemos el token desde las variables de entorno
TOKEN = os.getenv("DISCORD_TOKEN")

# Ejecutamos el bot
bot.run(TOKEN)
