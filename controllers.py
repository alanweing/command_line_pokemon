from models import Player
from functions import die

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
