from pymysql import connect, err, cursors
import _print
from _input import Input
import env


# classe que mantém a conexão com o banco armazenada
class MariaDB:

    def __init__(self):
        # aqui a conexão é realizada
        try:
            self.connection = connect(env.HOST, env.USER, env.PASSWORD, env.DB,
                                      charset='utf8',
                                      cursorclass=cursors.DictCursor)
        # se algo acontecer aqui é porque as credenciais passadas em env.py
        # estão erradas ou o RDMS está desligado
        except err.OperationalError as error:
            _print.danger('Database access denied!')
            _print.warning(str(error))
            exit(1)
        # se o banco não existir no RDBMS o exception abaixo é gerado
        except err.InternalError as error:
            if error.args[0] == 1049:
                _print.danger('The database "{}" does not exist!'
                              .format(env.DB))
                self.create_database()
            else:
                _print.danger('Database error!')
                _print.warning(str(error))
                exit(1)

    # se o banco não existir e o usuário quiser que o banco seja
    # automaticamente criado
    def create_database(self):
        if Input().get(_print.question('Do you want to create the \
database? [y/n]'), 'string', ['y', 'n']) == 'y':
            temp_connection = connect(env.HOST, env.USER, env.PASSWORD,
                                      charset='utf8',
                                      cursorclass=cursors.DictCursor)
            fd = open('pokedex.sql', 'r')
            sqlFile = fd.read()
            fd.close()
            sqlCommands = sqlFile.split(';')
            with temp_connection.cursor() as cursor:
                for command in sqlCommands:
                    try:
                        cursor.execute(command)
                    except err.OperationalError as msg:
                        print("Command skipped:", msg)
                    except err.MySQLError as error:
                        _print.danger('Database error!')
                        _print.warning(str(error))
                        exit(1)
                temp_connection.commit()
                _print.success('Database successfully created!')
                self.__init__()
        else:
            exit(0)
