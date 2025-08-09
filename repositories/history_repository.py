from models.history import History
from models.usuario import Usuario
from basededatos import get_db_connection

class HistoryRepository:
    def get_by_user(self, usuario: Usuario):   
        histories_db = []
        with get_db_connection() as conexion:
            cursorBD = conexion.cursor()
            cursorBD.execute("SELECT * FROM historial WHERE id_usuario = ?", (usuario.id,))
            histories_db = cursorBD.fetchall() #viene como lista de tuplas
        
        histories =  []
        for h in histories_db:
            histories.append(History(h[0], h[1], h[2], h[3], h[4], h[5]))
        return histories

            
    def insertar(self, id_usuario, id_pregunta,coins, fecha, respuesta):
        with get_db_connection() as conexion:
            cursorBD = conexion.cursor()
            cursorBD.execute(
                "INSERT INTO historial (id_usuario, id_pregunta, coins, fecha, respuesta) VALUES (?, ?, ?, ?, ?)",
                (id_usuario, id_pregunta, coins, fecha, respuesta)
            )
            conexion.commit()
            return True
        