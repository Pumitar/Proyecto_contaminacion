import os
import threading
from command.bot import bot
from api.server import app
from dotenv import load_dotenv

# Cargamos las variables de entorno
load_dotenv()

# Obtenemos el token desde las variables de entorno
TOKEN = os.getenv("DISCORD_TOKEN")

# Ejecutamos el bot
def run_thread_2():
    app.run(port=3000, debug=True, use_reloader=False)
     
def run_thread_1():
    bot.run(TOKEN)


if __name__ == "__main__":
    # Crear un hilo para ejecutar la API de Flask
    thread_2 = threading.Thread(target=run_thread_2)
    thread_2.start()
    
    run_thread_1()



# *** En caso de que el proyecto se siga ejecutando en segundo plano 

# ### Listar procesos en el puerto 3000
# netstat -ano|findstr 3000

# ### ejemplo de respueta
# TCP    127.0.0.1:3000         0.0.0.0:0              LISTENING       20932

# ### Matar proceso 20932
# taskkill /f /pid 23228 

    
    
    
