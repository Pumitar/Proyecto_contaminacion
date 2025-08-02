import sqlite3  

class PreguntasRepository:
    def __init__(self):
        self.db_connection = sqlite3.connect("contaminacion.db")
        
    def obtener_pregunta_ecologica(self):
        cursorBD = self.db_connection.cursor()
        cursorBD.execute("SELECT * FROM preguntas ORDER BY RANDOM() LIMIT 1")
        return cursorBD.fetchone()
    
    def obtener_pregunta(self, id_pregunta):
        cursorBD = self.db_connection.cursor()
        cursorBD.execute("SELECT * FROM preguntas WHERE id = ?", (id_pregunta,))
        return cursorBD.fetchone()