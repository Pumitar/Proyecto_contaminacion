from models.usuario import Usuario
from repositories.usuarios_repository import UsuariosRepository

class UsuarioService:
    def __init__(self, usuario_repository:UsuariosRepository):
        self.usuario_repository = usuario_repository

    def crear(self, id_discord, username, display_name, avatar):
        user = Usuario(None, id_discord, username, display_name, avatar, coins = 0)
        is_created = self.usuario_repository.registrar_usuario(user)
        return user, is_created

    def obtener_por_username(self, username):
         return self.usuario_repository.get_usuario(username)

    def obtener_por_discord_id(self, id_discord):
         return self.usuario_repository.obtener_por_discord_id(id_discord)
     
    def obtener_ranking(self):
         return self.usuario_repository.obtener_ranking()
     
    def actualizar_coins(self, usuario:Usuario, coins:int):
        usuario.modificar_coins(coins)
        return self.usuario_repository.actualizar_coins(usuario)
    
    

