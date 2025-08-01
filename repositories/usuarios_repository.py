import sqlite3  
from models.usuario import Usuario
from basededatos import get_db_connection

class UsuariosRepository:
    def get_usuario(self, username):
        with get_db_connection() as conexion:
            cursorBD = conexion.cursor()
            cursorBD.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
            usuario_db = cursorBD.fetchone()
            if usuario_db:
                return Usuario(usuario_db[0], usuario_db[1], usuario_db[2], usuario_db[3])
            
            else:
                return None


    def registrar_usuario(self, user: Usuario):
        with get_db_connection() as conexion:
            cursorBD = conexion.cursor()
            try:
                cursorBD.execute(
                    "INSERT INTO usuarios (id_discord, username, coins) VALUES (?, ?, ?)",
                    (user.id_discord, user.username, user.coins)
                )
                conexion.commit()
                return True
            except sqlite3.IntegrityError:
                return False

        
    def obtener_ranked_usuarios(self, limit=10):
        with get_db_connection() as conexion:
            cursorBD = conexion.cursor() 
            cursorBD.execute("SELECT * FROM usuarios ORDER BY coins DESC LIMIT ?", (limit,))
            return cursorBD.fetchall()
    
    def actualizar_coins(self, user: Usuario):
        with get_db_connection() as conexion:
            cursorBD = conexion.cursor()
            cursorBD.execute(
                "UPDATE usuarios SET coins = ? WHERE id_discord = ?",
                (user.coins, user.id_discord)
            )
            conexion.commit()
            return True