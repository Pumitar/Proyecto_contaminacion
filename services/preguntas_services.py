from repositories.preguntas_repository import PreguntasRepository


class PreguntaService:
    def __init__(self, pregunta_repository:PreguntasRepository):
        self.pregunta_repository = pregunta_repository

    def obtener_pregunta_random(self):
        return self.pregunta_repository.obtener_pregunta_random()
    
    def obtener_pregunta(self, id_pregunta):
        return self.pregunta_repository.obtener_pregunta(id_pregunta)