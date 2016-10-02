from models import Player, Pokemon, PlayerPokemon
from functions import die
from numpy import random
from threading import Thread
import env

class PlayerController:

    def __init__(self):
        self.player = None
        self.login = None
        self.token = None
        self.pokemons = None

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
        return True if result is not False else False

    def pokemons(self):
        result = self.pokemons

    def add_pokemon(self, login, pokemon):
        PlayerPokemon().create({'player_login': login, 'pokemon_name': pokemon, 'name': pokemon})
        if pokemon['name'] == 'Egg':
            egg = PlayerPokemon().first('pokemon_name="Egg" AND player_login="{}"'.format(self.login), order_by='created_at DESC')
            listener = Thread(target=self.egg_listener, args=(egg,)).start()
            self.add_egg_listener(egg)
        self.pokemons = PlayerPokemon().where('player_login="{}"'.format(self.login))

    @staticmethod
    def egg_listener(egg):
        from time import sleep
        sleep(env.EGG_HATCH_TIME)
        self.hatch_egg(egg)

    def hatch_egg(self, egg):
        pass


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
