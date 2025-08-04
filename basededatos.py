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
        "SELECT COUNT(id) FROM preguntas WHERE pregunta=?",
        (pregunta,)
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
    {"pregunta": "¿Qué tipo de bolsa contamina más: tela o plástico?", "respuesta": "plástico", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿En qué mes se celebra el Día Mundial del Medio Ambiente?", "respuesta": "junio", "ganancia": 50, "perdida": -25},
    {"pregunta": "¿Qué animal representa la contaminación por petróleo en los mares?", "respuesta": "pingüino", "ganancia": 85, "perdida": -43},
    {"pregunta": "¿Qué día se celebra el Día de la Tierra? (escribe solo el número)", "respuesta": "22", "ganancia": 70, "perdida": -35},
    {"pregunta": "¿Qué planeta del sistema solar está habitado por humanos?", "respuesta": "Tierra", "ganancia": 95, "perdida": -48},
    {"pregunta": "¿Qué gas produce la ganadería intensiva?", "respuesta": "metano", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Cuál es una fuente de energía renovable: solar o carbón?", "respuesta": "solar", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Cuál es la R que significa usar algo otra vez?", "respuesta": "reutilizar", "ganancia": 70, "perdida": -35},
    {"pregunta": "¿Qué líquido esencial se contamina con desechos industriales?", "respuesta": "agua", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué gas respiran las plantas para hacer la fotosíntesis?", "respuesta": "co2", "ganancia": 65, "perdida": -32},
    {"pregunta": "¿Qué aparato convierte la energía solar en electricidad?", "respuesta": "panel solar", "ganancia": 95, "perdida": -47},
    {"pregunta": "¿Qué electrodoméstico consume más energía en casa?", "respuesta": "refrigeradora", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué animal está en peligro por el plástico en el mar: tortuga o gallina?", "respuesta": "tortuga", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Cuál es el material más fácil de reciclar?", "respuesta": "papel", "ganancia": 65, "perdida": -32},
    {"pregunta": "¿Qué debemos hacer con el agua mientras lavamos los dientes?", "respuesta": "cerrarla", "ganancia": 75, "perdida": -37},
    {"pregunta": "¿Cuál es la temperatura ideal del aire acondicionado para ahorrar energía? (responde con número)", "respuesta": "24", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué parte del cuerpo del pez globo se hincha para defenderse?", "respuesta": "cuerpo", "ganancia": 50, "perdida": -25},
    {"pregunta": "¿Cómo se llama el proceso de convertir basura en nuevos productos?", "respuesta": "reciclaje", "ganancia": 60, "perdida": -30},
    {"pregunta": "¿Qué tipo de energía se obtiene del viento?", "respuesta": "eólica", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Cuál es el país con más deforestación del mundo? (Brasil o Canadá)", "respuesta": "brasil", "ganancia": 70, "perdida": -35},
    {"pregunta": "¿Qué se debe hacer con las pilas usadas: reciclarlas o tirarlas a la basura?", "respuesta": "reciclarlas", "ganancia": 100, "perdida": -50},
    {"pregunta": "¿Qué tipo de energía NO contamina: solar o petróleo?", "respuesta": "solar", "ganancia": 75, "perdida": -37},
    {"pregunta": "¿Qué tipo de luz consume menos electricidad?", "respuesta": "led", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Qué se debe hacer con las botellas plásticas usadas?", "respuesta": "reciclar", "ganancia": 65, "perdida": -32},
    {"pregunta": "¿Qué acción ayuda a reducir la huella de carbono: caminar o usar auto?", "respuesta": "caminar", "ganancia": 70, "perdida": -35},
    {"pregunta": "¿Qué aparato se debe apagar si no se usa?", "respuesta": "luces", "ganancia": 60, "perdida": -30},
    {"pregunta": "¿Qué planeta tiene vida confirmada?", "respuesta": "tierra", "ganancia": 95, "perdida": -47},
    {"pregunta": "¿Qué usamos para beber agua sin contaminar con plásticos?", "respuesta": "botella reutilizable", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué animal marino se enreda con redes y muere?", "respuesta": "tortuga", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué día del año se celebra el Día del Medio Ambiente?", "respuesta": "5", "ganancia": 60, "perdida": -30},
    {"pregunta": "¿Qué podemos hacer con ropa que ya no usamos?", "respuesta": "donar", "ganancia": 70, "perdida": -35},
    {"pregunta": "¿Qué gas expulsan los autos?", "respuesta": "CO2", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Qué produce más CO2: avión o bicicleta?", "respuesta": "avión", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué podemos hacer con el papel usado?", "respuesta": "reciclar", "ganancia": 60, "perdida": -30},
    {"pregunta": "¿Qué aparato convierte energía eólica en electricidad?", "respuesta": "aerogenerador", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué debemos hacer con el aceite de cocina usado?", "respuesta": "reciclar", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Qué es mejor para el planeta: duchas cortas o largas?", "respuesta": "cortas", "ganancia": 75, "perdida": -37},
    {"pregunta": "¿Qué animal sufre por la caza ilegal de marfil?", "respuesta": "elefante", "ganancia": 100, "perdida": -50},
    {"pregunta": "¿Qué acción ayuda más al ambiente: plantar árboles o cortar árboles?", "respuesta": "plantar árboles", "ganancia": 95, "perdida": -47},
    {"pregunta": "¿Qué gas se encuentra en los refrigeradores antiguos y daña la capa de ozono?", "respuesta": "clorofluorocarbono", "ganancia": 100, "perdida": -50},
    {"pregunta": "¿Qué hacemos al reutilizar?", "respuesta": "usar de nuevo", "ganancia": 65, "perdida": -32},
    {"pregunta": "¿Qué tipo de energía viene del agua?", "respuesta": "hidroeléctrica", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué es más sostenible: transporte público o coche privado?", "respuesta": "transporte público", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué tipo de residuos van al contenedor azul?", "respuesta": "papel", "ganancia": 70, "perdida": -35},
    {"pregunta": "¿Qué animal marino confunde bolsas plásticas con medusas?", "respuesta": "tortuga", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué es mejor para reducir residuos: comprar a granel o empaquetado?", "respuesta": "a granel", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué debemos evitar para cuidar los océanos?", "respuesta": "tirar basura", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Qué parte de la atmósfera protege del sol?", "respuesta": "capa de ozono", "ganancia": 100, "perdida": -50},
    {"pregunta": "¿Qué se usa para medir la calidad del aire?", "respuesta": "índice de contaminación", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué acción ayuda a conservar energía en casa?", "respuesta": "apagar luces", "ganancia": 75, "perdida": -37},
    {"pregunta": "¿Qué contaminante es común en ríos por detergentes?", "respuesta": "fosfatos", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué animal está en peligro por el deshielo?", "respuesta": "oso polar", "ganancia": 95, "perdida": -47},
    {"pregunta": "¿Qué transporte contamina menos?", "respuesta": "bicicleta", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué debemos hacer con los residuos orgánicos?", "respuesta": "compostar", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Qué tipo de energía se genera a partir de restos vegetales?", "respuesta": "biomasa", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Cuál es el gas más abundante en la atmósfera?", "respuesta": "nitrógeno", "ganancia": 70, "perdida": -35},
    {"pregunta": "¿Qué animal está en peligro por el deshielo polar?", "respuesta": "oso polar", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué medio de transporte no contamina?", "respuesta": "bicicleta", "ganancia": 75, "perdida": -37},
    {"pregunta": "¿Qué debemos hacer con los electrónicos viejos?", "respuesta": "reciclar", "ganancia": 95, "perdida": -47},
    {"pregunta": "¿Qué es más ecológico: papel reciclado o papel nuevo?", "respuesta": "papel reciclado", "ganancia": 60, "perdida": -30},
    {"pregunta": "¿Qué insecto ayuda a polinizar flores?", "respuesta": "abeja", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Cuál es la principal causa de la lluvia ácida?", "respuesta": "contaminación del aire", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué significa el símbolo ♻️?", "respuesta": "reciclaje", "ganancia": 65, "perdida": -32},
    {"pregunta": "¿Qué tipo de productos debemos evitar para reducir residuos?", "respuesta": "desechables", "ganancia": 75, "perdida": -37},
    {"pregunta": "¿Qué tipo de bolsa es reutilizable?", "respuesta": "tela", "ganancia": 70, "perdida": -35},
    {"pregunta": "¿Cuál es el nombre del agujero en la atmósfera?", "respuesta": "capa de ozono", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Qué material se usa para hacer compost?", "respuesta": "residuos orgánicos", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué país tiene más biodiversidad?", "respuesta": "Brasil", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué hacemos al reciclar papel?", "respuesta": "salvamos arboles", "ganancia": 95, "perdida": -47},
    {"pregunta": "¿Qué significa consumir de forma sostenible?", "respuesta": "pensar en el ambiente", "ganancia": 100, "perdida": -50},
    {"pregunta": "¿Qué podemos hacer con las cáscaras de frutas?", "respuesta": "compostar", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Qué tipo de bombilla dura más?", "respuesta": "led", "ganancia": 60, "perdida": -30},
    {"pregunta": "¿Qué animal necesita hielo para sobrevivir?", "respuesta": "oso polar", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué debemos hacer para proteger los bosques?", "respuesta": "no talar arboles", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué podemos hacer con una botella de vidrio?", "respuesta": "reciclar", "ganancia": 95, "perdida": -47},
    {"pregunta": "¿Qué debemos hacer con los envases de cartón?", "respuesta": "reciclar", "ganancia": 70, "perdida": -35},
    {"pregunta": "¿Qué especie marina come plásticos por error?", "respuesta": "tortuga", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Qué país genera más residuos por persona?", "respuesta": "eeuu", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué podemos hacer para reducir el consumo de energía?", "respuesta": "apagar luces", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué significa energía limpia?", "respuesta": "no contamina", "ganancia": 95, "perdida": -47},
    {"pregunta": "¿Qué podemos hacer para cuidar el planeta?", "respuesta": "reciclar", "ganancia": 100, "perdida": -50},
    {"pregunta": "¿Qué tipo de agua es potable?", "respuesta": "agua limpia", "ganancia": 70, "perdida": -35},
    {"pregunta": "¿Qué es mejor: comprar local o importado?", "respuesta": "local", "ganancia": 60, "perdida": -30},
    {"pregunta": "¿Qué podemos hacer para evitar la contaminación del mar?", "respuesta": "no tirar basura", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué animal marino es muy afectado por el plástico?", "respuesta": "tortuga", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué aparato convierte el sol en energía?", "respuesta": "panel solar", "ganancia": 95, "perdida": -47},
    {"pregunta": "¿Qué acción es parte de las 3R?", "respuesta": "reducir", "ganancia": 100, "perdida": -50},
    {"pregunta": "¿Qué tipo de pila contamina más?", "respuesta": "pila alcalina", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Qué debemos evitar para cuidar el aire?", "respuesta": "quema de basura", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué podemos hacer con las latas?", "respuesta": "reciclar", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué tipo de productos generan menos residuos?", "respuesta": "a granel", "ganancia": 95, "perdida": -47},
    {"pregunta": "¿Qué debemos hacer con las bolsas de supermercado?", "respuesta": "reutilizarlas", "ganancia": 100, "perdida": -50},
    {"pregunta": "¿Qué gas expulsamos al respirar?", "respuesta": "CO2", "ganancia": 80, "perdida": -40},
    {"pregunta": "¿Qué árbol es símbolo de oxígeno?", "respuesta": "árbol", "ganancia": 75, "perdida": -37},
    {"pregunta": "¿Qué debemos hacer con los residuos reciclables?", "respuesta": "separarlos", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué debemos evitar para cuidar la fauna?", "respuesta": "caza", "ganancia": 90, "perdida": -45},
    {"pregunta": "¿Qué causa la contaminación acústica?", "respuesta": "ruido", "ganancia": 95, "perdida": -47},
    {"pregunta": "¿Qué debemos hacer con el papel en buen estado?", "respuesta": "reutilizar", "ganancia": 60, "perdida": -30},
    {"pregunta": "¿Qué significa 'huella ecológica'?", "respuesta": "impacto ambiental", "ganancia": 85, "perdida": -42},
    {"pregunta": "¿Qué debemos evitar para cuidar los ríos?", "respuesta": "tirar basura", "ganancia": 100, "perdida": -50}

]



tabla_usuarios()
tabla_preguntas()
tabla_historial()

for p in preguntas:
    insertar_pregunta(p["pregunta"], p["respuesta"], p["ganancia"], p["perdida"])