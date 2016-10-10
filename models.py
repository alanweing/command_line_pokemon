from model import Model

# cada model implementado abaixo representa uma tabela do banco de dados, dessa
# forma o acesso é mais fácil.
# Cada model precisa passar ao construtor do Model a tabela que ele representa
# junto das colunes que possui. Além disso, precisam sobreescrever os campos
# que podem ser preenchidos (self.fillable), a chave primária (se for diferente
# de 'id'(self.primary_key)).
# depois disso, todos as funções em Model podem ser acessadas.


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
        # name representa um nome dado ao pokemon pelo usuário


class Type(Model):

    def __init__(self):
        super().__init__(table='type', fields=['name'])
        self.primary_key = 'name'
        self.fillable = ['name']


class Weakness(Model):

    def __init__(self):
        super().__init__(table='type_damage', fields=['attacking_type',
                                                      'defending_type',
                                                      'damage_multiplier'])
        self.primary_key = 'attacking_type'
        self.fillable = ['attacking_type', 'defending_type',
                         'damage_multiplier']
