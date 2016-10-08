from models import Player, Pokemon, PlayerPokemon, PokemonType
from functions import die
from numpy import random
from threading import Thread
from _input import Input
import _print
import env

class PlayerController:

    def __init__(self):
        self.player = None
        self.login = None
        self.token = None
        self.pokemons = []

    def create(self, login, password):
        from hashlib import sha512, sha256
        import time
        self.player = Player()
        hashed_password = sha512()
        hashed_password.update(password.encode('utf8'))
        hashed_password = hashed_password.hexdigest()
        token = sha256()
        token.update((str(time.time()) + login).encode('utf8'))
        token = token.hexdigest()
        result = self.player.create(login, hashed_password, token)
        if result is not False:
            self.login = login
            self.token = token
        return True if result is not False else False

    def authorize(self, login, password):
        from hashlib import sha512
        self.player = Player()
        hashed_password = sha512()
        hashed_password.update(password.encode('utf8'))
        hashed_password = hashed_password.hexdigest()
        result = self.player.authorize(login, hashed_password)
        if result is not False:
            self.login = login
            self.token = result['token']
            self.pokemons = PlayerPokemon().where('player_login="{}"'.format(self.login))
            self.extend_pokemon_info()
        return True if result is not False else False

    def get_pokemons(self):
        return self.pokemons

    def add_pokemon(self, login, pokemon):
        double_name = PlayerPokemon().where('player_login="{}" AND name="{}"'.format(self.login, pokemon))
        if len(double_name) != 0:
            _print.info("You can't have two pokemons with the same name!")
            print('You need to give {} ({}) a new name'.format(double_name[0]['name'], double_name[0]['pokemon_name']))
            self.rename_pokemon(double_name[0]['name'])
        PlayerPokemon().create({'player_login': login, 'pokemon_name': pokemon, 'name': pokemon})
        if pokemon == 'Egg':
            egg = PlayerPokemon().first(conditions='pokemon_name="Egg" AND player_login="{}"'.format(self.login), order_by='created_at DESC')
            listener = Thread(target=self.egg_listener, args=(egg,)).start()
        self.refresh_pokemon_list()

    def egg_listener(self, egg):
        from time import sleep
        sleep(env.EGG_HATCH_TIME)
        self.hatch_egg(egg)

    def hatch_egg(self, egg):
        new_pokemon = Pokemon().where('rarity="very common"')
        new_pokemon = new_pokemon[random.choice(len(new_pokemon), 1)[0]]
        PlayerPokemon().update('pokemon_name="{}"'.format(new_pokemon['name']), egg['id'])
        _print.success('One of your eggs hatched! New pokemon: {}'.format(new_pokemon['name']))
        self.refresh_pokemon_list()

    def rename_pokemon(self, pokemon_name):
        pokemon_entry = PlayerPokemon().where('player_login="{}" AND name="{}"'.format(self.login, pokemon_name))
        if len(pokemon_entry) == 0:
            _print.warning('You have no pokemon called "{}"'.format(pokemon_name))
            return
        new_name = Input()
        new_name.get(_print.question('Choose a new name:'), 'string', None)
        while not self.check_pokemon_name(new_name.last_input):
            _print.colorize('You alredy have a pokemon named "{}"'.format(new_name.last_input), _print.Color.RED)
            new_name.get(_print.question('Choose a new name:'), 'string', None)
        PlayerPokemon().update('name="{}"'.format(new_name.last_input), pokemon_entry[0]['id'])
        self.refresh_pokemon_list()

    def check_pokemon_name(self, name):
        pokemon_entry = PlayerPokemon().where('player_login="{}" AND name="{}"'.format(self.login, name))
        return True if len(pokemon_entry) == 0 else False

    def refresh_pokemon_list(self):
        self.pokemons = PlayerPokemon().where('player_login="{}"'.format(self.login))
        self.extend_pokemon_info()
        self.sort_pokemons('pokemon_name')

    def order_pokemons(self):
        _print.colorize('You can order by: name, pokemon, rarity and type', _print.Color.BLUE)
        order_by = Input()
        order_by = order_by.get('Order by:', 'string', ['name', 'pokemon', 'rarity', 'type'])
        if order_by == 'pokemon':
            self.sort_pokemons('pokemon_name')
        elif order_by == 'type' or order_by == 'rarity':
            print(self.sort_pokemons('type', vio=True))
            exit(0)
        else:
            self.sort_pokemons(order_by)

    def sort_pokemons(self, order_by, vio=False):
        from functions import _sort
        names = []
        for pokemon in self.pokemons:
            names.append(pokemon[order_by])
        names = _sort(names)
        aux_list = self.pokemons
        i = 0
        if not vio:
            self.pokemons = []
        else:
            list_index = []
        for name in names:
            for pokemon in aux_list:
                if pokemon[order_by] == name:
                    if not vio:
                        self.pokemons.append(pokemon)
                    else:
                        list_index.append(i)
                    print(pokemon[order_by])
                    del(aux_list[i])
                i += 1
            i = 0
        if vio:
            return list_index


    def extend_pokemon_info(self):
        for pokemon in self.pokemons:
            pokemon['rarity'] = Pokemon().find(pokemon['pokemon_name'])['rarity']
            pokemon['type'] = PokemonType().first(conditions='pokemon_name="{}"'.format(pokemon['pokemon_name']))['type_name']

    def list_pokemons(self):
        for pokemon in self.pokemons:
            print('***-***-***-***')
            print('Pokemon: {}'.format(pokemon['pokemon_name']))
            print('Cathed at: {}'.format(pokemon['created_at'].strftime('%d/%m/%Y %H:%M:%S')))
            print('Rarity: {}'.format(pokemon['rarity'].capitalize()))
            print('Name: {}'.format(pokemon['name']))
            print('Type: {}'.format(pokemon['type']))
            # ADD TYPE!
            print('***-***-***-***')


class PokemonController:

    rarity = [
        'very common',
        'common',
        'uncommon',
        'rare',
        'very rare',
        'special',
        'epic',
        'legendary',
        'egg',
        None
    ]

    def __init__(self):
        PokemonController.probability = [
            env.SPAWN_RATIO_RARITY_VERY_COMMON,
            env.SPAWN_RATIO_RARITY_COMMON,
            env.SPAWN_RATIO_RARITY_UNCOMMON,
            env.SPAWN_RATIO_RARITY_RARE,
            env.SPAWN_RATIO_RARITY_VERY_RARE,
            env.SPAWN_RATIO_RARITY_SPECIAL,
            env.SPAWN_RATIO_RARITY_EPIC,
            env.SPAWN_RATIO_RARITY_LEGENDARY,
            env.SPAWN_RATIO_EGG,
            1 - self.probability_sum()
        ]

    @staticmethod
    def hunt():
        pokemon_rarity = random.choice(PokemonController.rarity, 1, p=PokemonController.probability)
        if pokemon_rarity[0] is not None:
            if pokemon_rarity[0] == 'egg':
                return Pokemon().find('Egg')
            pokemon_model = Pokemon()
            pokemon = pokemon_model.where('rarity="{}"'.format(pokemon_rarity[0]))
            if len(pokemon) == 0:
                return
            return pokemon[random.choice(len(pokemon), 1)[0]]

    @staticmethod
    def probability_sum():
        return env.SPAWN_RATIO_RARITY_VERY_COMMON +  \
            env.SPAWN_RATIO_RARITY_COMMON + \
            env.SPAWN_RATIO_RARITY_UNCOMMON + \
            env.SPAWN_RATIO_RARITY_RARE + \
            env.SPAWN_RATIO_RARITY_VERY_RARE + \
            env.SPAWN_RATIO_RARITY_SPECIAL + \
            env.SPAWN_RATIO_RARITY_EPIC + \
            env.SPAWN_RATIO_RARITY_LEGENDARY +\
            env.SPAWN_RATIO_EGG
