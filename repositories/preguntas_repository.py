import sqlite3

from models.pregunta import Pregunta  

class PreguntasRepository:
    def __init__(self):
        self.db_connection = sqlite3.connect("contaminacion.db")
        
    def obtener_pregunta_random(self):
        cursorBD = self.db_connection.cursor()
        cursorBD.execute("SELECT * FROM preguntas ORDER BY RANDOM() LIMIT 1")
        pregunta_db = cursorBD.fetchone()
        if pregunta_db:
            return Pregunta(pregunta_db[0], pregunta_db[1], pregunta_db[2], pregunta_db[3], pregunta_db[4])
            
        else:
            return None
    
    def obtener_pregunta(self, id_pregunta):
        cursorBD = self.db_connection.cursor()
        cursorBD.execute("SELECT * FROM preguntas WHERE id = ?", (id_pregunta,))
        pregunta_db = cursorBD.fetchone()
        if pregunta_db:
            return Pregunta(pregunta_db[0], pregunta_db[1], pregunta_db[2], pregunta_db[3], pregunta_db[4])
            
        else:
            return None
    