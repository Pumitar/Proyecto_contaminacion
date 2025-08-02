from models.usuario import Usuario
from basededatos import get_db_connection

class HistoryRepository:
    def get_by_user(self, usuario: Usuario):
        with get_db_connection() as conexion:
            cursorBD = conexion.cursor()
            cursorBD.execute("SELECT * FROM historial WHERE id_usuario = ?", (usuario.id,))
            return cursorBD.fetchall()

    def insert_history(self, id_usuario, id_pregunta,coins, fecha, respuesta):
        with get_db_connection() as conexion:
            cursorBD = conexion.cursor()
            cursorBD.execute(
                "INSERT INTO historial (id_usuario, id_pregunta, coins, fecha, respuesta) VALUES (?, ?, ?, ?, ?)",
                (id_usuario, id_pregunta, coins, fecha, respuesta)
            )
            conexion.commit()
            return True
        