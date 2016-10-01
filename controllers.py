from models import Player
from functions import die
from numpy import random
import env

class PlayerController:

    @staticmethod
    def create(login, password):
        new_player = Player()
        from hashlib import sha512, sha256
        import time
        hashed_password = sha512()
        hashed_password.update(password.encode('utf8'))
        hashed_password = hashed_password.hexdigest()
        token = sha256()
        token.update((str(time.time()) + login).encode('utf8'))
        token = token.hexdigest()
        new_player.create(login, hashed_password, token)
        return new_player

    @staticmethod
    def authorize(login, password):
        from hashlib import sha512
        hashed_password = sha512()
        hashed_password.update(password.encode('utf8'))
        hashed_password = hashed_password.hexdigest()
        player = Player()
        authorized = player.authorize(login, hashed_password)
        return player, authorized


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
            1 - self.probability_sum()
        ]

    @staticmethod
    def hunt():
        prey = random.choice(PokemonController.rarity, 1, p=PokemonController.probability)
        print(prey)

    @staticmethod
    def probability_sum():
        return env.SPAWN_RATIO_RARITY_VERY_COMMON +  \
            env.SPAWN_RATIO_RARITY_COMMON + \
            env.SPAWN_RATIO_RARITY_UNCOMMON + \
            env.SPAWN_RATIO_RARITY_RARE + \
            env.SPAWN_RATIO_RARITY_VERY_RARE + \
            env.SPAWN_RATIO_RARITY_SPECIAL + \
            env.SPAWN_RATIO_RARITY_EPIC + \
            env.SPAWN_RATIO_RARITY_LEGENDARY