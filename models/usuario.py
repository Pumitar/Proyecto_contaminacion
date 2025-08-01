class Usuario:
    def __init__(self, id, id_discord, username, coins=100):
        self.id_discord = id_discord
        self.username = username
        self.coins = coins
        self.id = id

    def __repr__(self):
        return f"Usuario(id={self.id}, id_discord={self.id_discord}, usuario='{self.username}', coins={self.coins})"
    
    def modificar_coins(self, coins):
        self.coins += coins
        return self.coins
    
