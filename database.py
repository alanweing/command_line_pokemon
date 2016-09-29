from pymysql import connect, err, cursors
import _print
import env


class MariaDB:

    def __init__(self):
        try:
            self.connection = connect(env.HOST, env.USER, env.PASSWORD, env.DB, charset='utf8', cursorclass=cursors.DictCursor)
        except err.OperationalError as error:
            _print.danger('Database access denied!')
            _print.warning(str(error))
            exit(1)

    def create_player(self, login, password):
        from hashlib import sha512, sha256
        import time
        _hash = sha512()
        _hash.update(password.encode('utf8'))
        _hash = _hash.hexdigest()
        token = sha256()
        token.update(str(time.time()).encode('utf8'))
        token = token.hexdigest()
        with self.connection.cursor() as cursor:
            try:
                cursor.execute('INSERT INTO pokedex.players (login, password, token) VALUES(%s, %s, %s)', (login, _hash, token))
                self.connection.commit()
            except err.MySQLError as error:
                self.connection.rollback()
                _print.danger('Database error!')
                if env.DEBUG:
                    if error.args[0] == 1062:
                        _print.warning('This username already exists!')
                return False
            return True
