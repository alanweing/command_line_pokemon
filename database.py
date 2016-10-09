from pymysql import connect, err, cursors
import _print
import env


class MariaDB:

    def __init__(self):
        try:
            self.connection = connect(env.HOST, env.USER, env.PASSWORD, env.DB,
                                      charset='utf8',
                                      cursorclass=cursors.DictCursor)
        except err.OperationalError as error:
            _print.danger('Database access denied!')
            _print.warning(str(error))
            exit(1)
