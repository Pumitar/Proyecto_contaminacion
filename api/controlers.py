import json
from repositories.usuarios_repository import UsuariosRepository
from services.usuarios_services import UsuarioService


usuarios_services = UsuarioService(UsuariosRepository())

def serialize_user(user):
    return {
        'display_name': user.display_name,
        'coins': user.coins,
        'avatar': user.avatar
    }
    
    
def get_ranking():
    ranking = usuarios_services.obtener_ranking()
    serialized_ranking = [serialize_user(user) for user in ranking]
    return serialized_ranking
