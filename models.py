from model import Model


class Player(Model):

    def __init__(self):
        super().__init__(table='players', fields=['login', 'password', 'token', 'pokebolls', 'experience', 'level'])
        self.fillable = ['login', 'password', 'token']
        self.primary_key = 'login'
        self.token = None

    def create(self, login, password, token):
        result = super().create({'login': login, 'password': password, 'token': token})
        if result is not False:
            self.login = login
            self.token = token
        return result

    def authorize(self, login, password):
        result = self.find(login, conditions="password='{}'".format(password), fields='token')
        if result is not False:
            self.login = login
            self.token = result['token']
        return result


class Pokemon:

    def __init__(self, db_connection):
        self.fields = ['name', 'rarity', 'evolves_from', 'type', 'combat_power']
        self.db_connection = db_connection


class Type:

    def __init__(self, db_connection):
        self.fields = ['name']
        self.db_connection = db_connection
