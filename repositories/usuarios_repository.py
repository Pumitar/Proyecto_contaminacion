import sqlite3  

class UsuariosRepository:
    def __init__(self):
        self.db_connection = sqlite3.connect("contaminacion.db")


    def get_usuario(self, username):
        cursorBD = self.db_connection.cursor()
        cursorBD.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        return cursorBD.fetchone()


    def registrar_usuario(self, id_discord, usuario):
        cursorBD = self.db_connection.cursor()
        try:
            cursorBD.execute(
                "INSERT INTO usuarios (id_discord, usuario, coins) VALUES (?, ?, ?)",
                (id_discord, usuario, 0)
            )
            self.db_connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

        
    def obtener_ranked_usuarios(self, limit=10):
        cursorBD = self.db_connection.cursor()  
        cursorBD.execute("SELECT * FROM usuarios ORDER BY coins DESC LIMIT ?", (limit,))
        return cursorBD.fetchall()
    