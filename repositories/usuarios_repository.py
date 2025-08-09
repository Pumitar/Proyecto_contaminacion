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
                return Usuario(usuario_db[0], usuario_db[1], usuario_db[2], usuario_db[3], usuario_db[4], usuario_db[5])
            
            else:
                return None


    def registrar_usuario(self, user: Usuario):
        with get_db_connection() as conexion:
            cursorBD = conexion.cursor()
            try:
                cursorBD.execute(
                    "INSERT INTO usuarios (id_discord, username, display_name, avatar, coins) VALUES (?, ?, ?, ?, ?)",
                    (user.id_discord, user.username, user.display_name, user.avatar, user.coins)
                )
                conexion.commit()
                return True
            except sqlite3.IntegrityError:
                return False
        
    def obtener_ranking(self, limit=10):
        usuarios_db = []
        with get_db_connection() as conexion:
            
            cursorBD = conexion.cursor() 
            cursorBD.execute("SELECT * FROM usuarios ORDER BY coins DESC LIMIT ?", (limit,))
            usuarios_db = cursorBD.fetchall() #viene como lista de tuplas
         
        usuarios =  []
        for u in usuarios_db:
            usuarios.append(Usuario(u[0], u[1], u[2], u[3], u[4], u[5]))
        return usuarios

    
    def actualizar_coins(self, user: Usuario):
        with get_db_connection() as conexion:
            cursorBD = conexion.cursor()
            cursorBD.execute(
                "UPDATE usuarios SET coins = ? WHERE id_discord = ?",
                (user.coins, user.id_discord)
            )
            conexion.commit()
            return True
        
    def obtener_por_discord_id(self, id_discord):
        with get_db_connection() as conexion:
            cursorBD = conexion.cursor()
            cursorBD.execute("SELECT * FROM usuarios WHERE id_discord = ?", (id_discord,))
            usuario_db = cursorBD.fetchone()
            if usuario_db:
                return Usuario(usuario_db[0], usuario_db[1], usuario_db[2], usuario_db[3], usuario_db[4], usuario_db[5])
            else:
                return None
            
