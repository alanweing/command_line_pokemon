from model import Model


class Player(Model):

    def __init__(self):
        super().__init__(table='players', fields=['login', 'password', 'token',
                         'pokebolls', 'experience', 'level'])
        self.fillable = ['login', 'password', 'token']
        self.primary_key = 'login'
        self.token = None

    def create(self, login, password, token):
        return super().create({'login': login, 'password': password,
                               'token': token})

    def authorize(self, login, password):
        return self.find(login, conditions="password='{}'".format(password),
                         fields='token')


class Pokemon(Model):

    def __init__(self):
        super().__init__(table='pokemons', fields=['name', 'category',
                                                   'rarity', 'ability',
                                                   'evolves_from', 'hp',
                                                   'attack', 'defense',
                                                   'special_attack',
                                                   'special_deffense',
                                                   'speed'])
        self.primary_key = 'name'
        self.fillable = self.fields


class PokemonType(Model):

    def __init__(self):
        super().__init__(table='pokemon_type', fields=['pokemon_name',
                                                       'pokemon_type'])
        self.primary_key = 'pokemon_name'
        self.fillable = ['pokemon_name', 'pokemon_type']


class PlayerPokemon(Model):

    def __init__(self):
        super().__init__(table='player_pokemon', fields=['id', 'player_login',
                                                               'pokemon_name',
                                                               'name',
                                                               'combat_power',
                                                               'created_at',
                                                               'updated_at'])
        self.fillable = ['player_login', 'pokemon_name', 'name']


class Type(Model):

    def __init__(self):
        super().__init__(table='type', fields=['name'])
        self.primary_key = 'name'
        self.fillable = ['name']
