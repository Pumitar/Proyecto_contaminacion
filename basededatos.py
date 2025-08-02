import sqlite3

conexion = sqlite3.connect("contaminacion.db")
cursorBD = conexion.cursor()

def get_db_connection():
    conexion = sqlite3.connect("contaminacion.db", timeout=20)
    conexion.row_factory = sqlite3.Row
    return conexion

def tabla_usuarios():
    cursorBD.execute(
        """SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name = '{}' """.format(
            "usuarios"
        )
    )
    if cursorBD.fetchone()[0] == 1:
        return True
    else:
        cursorBD.execute(
            """CREATE TABLE usuarios (id integer primary key autoincrement,id_discord integer unique, username text, coins integer) """
        )
        return False


def tabla_preguntas():
    cursorBD.execute(
        """SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name = '{}' """.format(
            "preguntas"
        )
    )
    if cursorBD.fetchone()[0] == 1:
        return True
    else:
        cursorBD.execute(
            """CREATE TABLE preguntas (id integer primary key autoincrement, pregunta text, respuesta text, ganancia integer, perdida integer) """
        )
        return False
    
def tabla_historial():
    cursorBD.execute(
        """SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name = '{}' """.format(
            "historial"
        )
    )
    if cursorBD.fetchone()[0] == 1:
        return True
    else:
        cursorBD.execute(
            """CREATE TABLE historial (id integer primary key autoincrement, id_usuario integer, id_pregunta integer, coins integer, fecha integer, respuesta text) """
        )
        return False


def insertar_pregunta(pregunta, respuesta, ganancia=0, perdida=0):
    cursorBD.execute(
        """SELECT COUNT(id) FROM preguntas WHERE pregunta='{}'""".format(
           pregunta
        )
    )
    if cursorBD.fetchone()[0] == 1:
        return True
    else:
        cursorBD.execute(
            "INSERT INTO preguntas (pregunta, respuesta, ganancia, perdida) VALUES (?, ?, ?, ?)",
            (pregunta, respuesta, ganancia, perdida),
        )
    conexion.commit()


preguntas = [
    {"pregunta": "¿Qué gas es el principal causante del efecto invernadero?", "respuesta": "co2", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Qué color de contenedor se usa para el vidrio?", "respuesta": "verde", "ganancia": 60, "perdida": -30},
    {"pregunta": "¿Cuál es una fuente de energía renovable: solar o carbón?", "respuesta": "solar", "ganancia": 70, "perdida": -35},
    {"pregunta": "¿Qué material es más contaminante: plástico o papel?", "respuesta": "plastico", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué día se celebra el Día de la Tierra? (escribe solo el número)", "respuesta": "22", "ganancia": 50, "perdida": -25},
    {"pregunta": "¿En qué mes se celebra el Día Mundial del Medio Ambiente?", "respuesta": "junio", "ganancia": 100, "perdida": -50},
    {"pregunta": "¿Cuál es el país con más deforestación del mundo? (Brasil o Canadá)", "respuesta": "brasil", "ganancia": 70, "perdida": -35},
    {"pregunta": "¿Cuál es el océano más contaminado del planeta?", "respuesta": "pacifico", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué tipo de bolsa contamina más: tela o plástico?", "respuesta": "plastico", "ganancia": 60, "perdida": -30},
    {"pregunta": "¿Qué animal está en peligro por el plástico en el mar: tortuga o gallina?", "respuesta": "tortuga", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Qué tipo de energía NO contamina: solar o petróleo?", "respuesta": "solar", "ganancia": 75, "perdida": -37},
    {"pregunta": "¿Cuál es la R que significa usar algo otra vez?", "respuesta": "reutilizar", "ganancia": 55, "perdida": -27},
    {"pregunta": "¿Cuál es la temperatura ideal del aire acondicionado para ahorrar energía? (responde con número)", "respuesta": "24", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué planeta estamos cuidando con estas acciones?", "respuesta": "tierra", "ganancia": 95, "perdida": -47},
    {"pregunta": "¿Qué se debe hacer con las pilas usadas: reciclarlas o tirarlas a la basura?", "respuesta": "reciclarlas", "ganancia": 100, "perdida": -50},

    {"pregunta": "¿Qué gas respiran las plantas para hacer la fotosíntesis?", "respuesta": "co2", "ganancia": 70, "perdida": -35},
    {"pregunta": "¿Cuál es el material más fácil de reciclar?", "respuesta": "papel", "ganancia": 65, "perdida": -32},
    {"pregunta": "¿Qué electrodoméstico consume más energía en casa?", "respuesta": "refrigeradora", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Cómo se llama el proceso de convertir basura en nuevos productos?", "respuesta": "reciclaje", "ganancia": 60, "perdida": -30},
    {"pregunta": "¿Qué gas produce la ganadería intensiva?", "respuesta": "metano", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué debemos hacer con el agua mientras lavamos los dientes?", "respuesta": "cerrarla", "ganancia": 75, "perdida": -37},
    {"pregunta": "¿Qué tipo de energía se obtiene del viento?", "respuesta": "eolica", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué animal representa la contaminación por petróleo en los mares?", "respuesta": "pinguino", "ganancia": 60, "perdida": -30},
    {"pregunta": "¿Qué parte del cuerpo del pez globo se hincha para defenderse?", "respuesta": "cuerpo", "ganancia": 50, "perdida": -25},
    {"pregunta": "¿Qué significa reducir en las 3R?", "respuesta": "consumir menos", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué país es uno de los líderes en energía solar?", "respuesta": "china", "ganancia": 100, "perdida": -50},
    {"pregunta": "¿Qué aparato convierte la energía solar en electricidad?", "respuesta": "panel solar", "ganancia": 95, "perdida": -47},
    {"pregunta": "¿Qué sucede cuando se talan muchos árboles?", "respuesta": "deforestacion", "ganancia": 75, "perdida": -37},
    {"pregunta": "¿Qué líquido esencial se contamina con desechos industriales?", "respuesta": "agua", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Qué planeta del sistema solar está habitado por humanos?", "respuesta": "tierra", "ganancia": 70, "perdida": -35}
]


tabla_usuarios()
tabla_preguntas()
tabla_historial()

for p in preguntas:
    insertar_pregunta(p["pregunta"], p["respuesta"], p["ganancia"], p["perdida"])