from model import Model


class Player(Model):

    def __init__(self):
        super().__init__(table='players', fields=['login', 'password', 'token', 'pokebolls', 'experience', 'level'])
        self.fillable = ['login', 'password', 'token']
        self.primary_key = 'name'

    def create(self, login, password, token):
        result = self.create({'login': login, 'password': password, 'token': token})




class Pokemon:

    def __init__(self, db_connection):
        self.fields = ['name', 'rarity', 'evolves_from', 'type', 'combat_power']
        self.db_connection = db_connection


class Type:

    def __init__(self, db_connection):
        self.fields = ['name']
        self.db_connection = db_connection
