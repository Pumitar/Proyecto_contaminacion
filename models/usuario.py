class Usuario:     
    def __init__(self, id, id_discord, username, display_name, avatar, coins=0):
        self.id = id
        self.id_discord = id_discord
        self.username = username
        self.display_name = display_name
        self.avatar = avatar

        self.coins = coins

    def __repr__(self):
        return f"Usuario(id={self.id}, id_discord={self.id_discord}, username='{self.username}', display_name='{self.display_name}', avatar='{self.avatar}', coins={self.coins})"
    
    def modificar_coins(self, coins):
        self.coins += coins
        return self.coins
    
    def info(self):
        return f"{self.display_name}, tienes {self.coins} eco-coins."
        