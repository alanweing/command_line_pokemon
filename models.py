from model import Model


class Player(Model):

    def __init__(self):
        super.__init__(table='players', fields=['login', 'password', 'token', 'pokebolls', 'experience', 'level'])

    def create(self, login, password):
        from hashlib import sha512, sha256
        import time
        _hash = sha512()
        _hash.update(password.encode('utf8'))
        _hash = _hash.hexdigest()
        token = sha256()
        token.update(str(time.time()).encode('utf8'))
        token = token.hexdigest()


class Pokemon:

    def __init__(self, db_connection):
        self.fields = ['name', 'rarity', 'evolves_from', 'type', 'combat_power']
        self.db_connection = db_connection


class Type:

    def __init__(self, db_connection):
        self.fields = ['name']
        self.db_connection = db_connection
