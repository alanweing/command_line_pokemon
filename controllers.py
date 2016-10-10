from models import Player, Pokemon, PlayerPokemon, PokemonType, Weakness
from functions import _sort
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
            self.pokemons = PlayerPokemon().where('player_login="{}"'
                                                  .format(self.login))
            self.extend_pokemon_info()
        return True if result is not False else False

    def get_pokemons(self):
        return self.pokemons

    def add_pokemon(self, pokemon):
        double_name = PlayerPokemon().where('player_login="{}" AND name="{}"'
                                            .format(self.login, pokemon))
        if len(double_name) != 0:
            _print.info("You can't have two pokemons with the same name!")
            print('You need to give {} ({}) a new name'
                  .format(double_name[0]['name'],
                          double_name[0]['pokemon_name']))
            self.rename_pokemon(double_name[0]['name'])
        PlayerPokemon().create({'player_login': self.login,
                               'pokemon_name': pokemon, 'name': pokemon})
        if pokemon == 'Egg':
            egg = PlayerPokemon().first(conditions='pokemon_name="Egg" AND \
                                        player_login="{}"'
                                        .format(self.login),
                                        order_by='created_at DESC')
            Thread(target=self.egg_listener, args=(egg,)).start()
        self.refresh_pokemon_list()

    def egg_listener(self, egg):
        from time import sleep
        sleep(env.EGG_HATCH_TIME)
        self.hatch_egg(egg)

    def hatch_egg(self, egg):
        new_pokemon = Pokemon().where('rarity="very common"')
        new_pokemon = new_pokemon[random.choice(len(new_pokemon), 1)[0]]
        PlayerPokemon().update('pokemon_name="{}"'
                               .format(new_pokemon['name']), egg['id'])
        _print.success('One of your eggs hatched! New pokemon: {}'
                       .format(new_pokemon['name']))
        self.refresh_pokemon_list()

    def rename_pokemon(self, pokemon_name):
        pokemon_entry = PlayerPokemon().where('player_login="{}" AND name="{}"'
                                              .format(self.login,
                                                      pokemon_name))
        if len(pokemon_entry) == 0:
            _print.warning('You have no pokemon called "{}"'
                           .format(pokemon_name))
            return
        new_name = Input()
        new_name.get(_print.question('Choose a new name:'), 'string', None)
        while not self.check_pokemon_name(new_name.last_input):
            _print.colorize('You alredy have a pokemon named "{}"'
                            .format(new_name.last_input), _print.Color.RED)
            new_name.get(_print.question('Choose a new name:'), 'string', None)
        PlayerPokemon().update('name="{}"'.format(new_name.last_input),
                               pokemon_entry[0]['id'])
        self.refresh_pokemon_list()

    def check_pokemon_name(self, name):
        pokemon_entry = PlayerPokemon().where('player_login="{}" AND name="{}"'
                                              .format(self.login, name))
        return True if len(pokemon_entry) == 0 else False

    def refresh_pokemon_list(self):
        self.pokemons = PlayerPokemon().where('player_login="{}"'
                                              .format(self.login))
        self.extend_pokemon_info()
        self.sort_pokemons('pokemon_name')

    def order_pokemons(self, order_by):
        if order_by == 'pokemon':
            self.sort_pokemons('pokemon_name')
        elif order_by == 'name':
            self.sort_pokemons(order_by)
        elif order_by == 'type' or order_by == 'rarity':
            vio = self.generate_vio(order_by)
            for index in vio:
                temp = self.pokemons[index]
                print('***-***-***-***')
                print('Pokemon: {}'.format(temp['pokemon_name']))
                print('Cathed at: {}'.format(temp['created_at']
                      .strftime('%d/%m/%Y %H:%M:%S')))
                print('Rarity: {}'.format(temp['rarity'].capitalize()))
                print('Name: {}'.format(temp['name']))
                print('Type: {}'.format(temp['type']))
                print('***-***-***-***')
        else:
            _print.colorize('Usage: pokemon sort name|pokemon|type|rarity\n\
                            name and pokemon name are physically sorted\n\
                            type and rarity are indirect arrays',
                            _print.Color.RED)

    def generate_vio(self, order_by):
        indexes = []
        names = []
        for pokemon in self.pokemons:
            names.append(pokemon[order_by])
        _sort(names)
        aux_list = []
        aux_list.extend(self.pokemons)
        i = 0
        temp = []
        for name in names:
            for pokemon in aux_list:
                if pokemon[order_by] == name and pokemon not in temp:
                    indexes.append(i)
                    temp.append(pokemon)
                i += 1
            i = 0
        return indexes

    def sort_pokemons(self, order_by):
        names = []
        for pokemon in self.pokemons:
            names.append(pokemon[order_by])
        names = _sort(names)
        aux_list = self.pokemons
        i = 0
        for name in names:
            for pokemon in aux_list:
                if pokemon[order_by] == name:
                    self.pokemons.append(pokemon)
                    del(aux_list[i])
                i += 1
            i = 0

    def extend_pokemon_info(self):
        for pokemon in self.pokemons:
            poke_temp = Pokemon().find(pokemon['pokemon_name'])
            pokemon['rarity'] = poke_temp['rarity']
            _type = PokemonType().first(conditions='pokemon_name="{}"'
                                        .format(pokemon['pokemon_name']))
            up = poke_temp
            while not _type:
                up = Pokemon().find(up['evolves_from'])
                _type = PokemonType().first(conditions='pokemon_name="{}"'
                                            .format(up['name']))
            pokemon['type'] = _type['type_name']

    def list_pokemons(self):
        for pokemon in self.pokemons:
            print('***-***-***-***')
            print('Pokemon: {}'.format(pokemon['pokemon_name']))
            print('Cathed at: {}'.format(pokemon['created_at']
                                         .strftime('%d/%m/%Y %H:%M:%S')))
            print('Rarity: {}'.format(pokemon['rarity'].capitalize()))
            print('Name: {}'.format(pokemon['name']))
            print('Type: {}'.format(pokemon['type']))
            print('***-***-***-***')

    def god_mode(self):
        opt = Input()
        opt.get(_print.question('This will override all your pokemons! \
Continue?'), 'string', ['yes', 'y', 'n', 'no'])
        if opt.last_input == 'yes' or opt.last_input == 'y':
            PlayerPokemon().delete('player_login="{}"'.format(self.login))
            for pokemon in Pokemon().select():
                if pokemon['name'] == 'Egg':
                    continue
                self.add_pokemon(pokemon['name'])
            _print.success('Bazinga!')


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
        pokemon_rarity = random.choice(PokemonController.rarity, 1,
                                       p=PokemonController.probability)
        if pokemon_rarity[0] is not None:
            if pokemon_rarity[0] == 'egg':
                return Pokemon().find('Egg')
            pokemon_model = Pokemon()
            pokemon = pokemon_model.where('rarity="{}"'
                                          .format(pokemon_rarity[0]))
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


class Battle:

    def __init__(self, player_pokemon, wild_pokemon):
        self.player_pokemon = Pokemon().find(player_pokemon['pokemon_name'])
        self.wild_pokemon = wild_pokemon
        get_pokemon_info(self.player_pokemon)
        get_pokemon_info(self.wild_pokemon)
        self.battling = True
        self.round = 0

    @staticmethod
    def get_pokemon_info(pokemon):
        _type = PokemonType().first(conditions='pokemon_name="{}"'
                                               .format(pokemon['name']))
        up = pokemon
        while not _type:
            up = Pokemon().find(up['evolves_from'])
            _type = PokemonType().first(conditions='pokemon_name="{}"'
                                                   .format(up['name']))
        pokemon['type'] = _type['type_name']
        pokemon['damage'] = Weakness().where('attacking_type="0" OR \
defending_type="{0}"'.format(_type['type_name']))

    def start(self):
        while self.battling
