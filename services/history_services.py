from models.usuario import Usuario
from repositories.history_repository import HistoryRepository

class HistoryService:
    def __init__(self, history_repository:HistoryRepository):
        self.history_repository = history_repository

    def insertar(self, id_usuario, id_pregunta,coins, fecha, respuesta):
        return self.history_repository.insertar(id_usuario, id_pregunta,coins, fecha, respuesta)
    
    def obtener_por_usuario(self, usuario:Usuario):
        return self.history_repository.get_by_user(usuario) 