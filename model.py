from database import MariaDB
from pymysql import err
import inspect
import _print
import env


# toda tabela do banco implementa a função Model, dessa forma tem acesso
# a todas as funções básicas. Model implementa MariaDB, isto é, tem uma conexão
# para cada model criado
class Model(MariaDB):

    def __init__(self, table, fields):
        super().__init__()
        # cada Model sabe a qual tabela pertence
        self.table = table
        # todos os campos pertencentes a tabela
        self.fields = fields
        # por padrão Model assume id como chave primária
        self.primary_key = 'id'
        # por padrão nenhum campo pode ser modificado
        self.fillable = []
        # se um erro for gerado, é armazenado nessa variável
        self.error_code = None
        # toda útlima query executada é armazenada aqui
        self.last_query = None

    # função de select, por padrão assume a seleção de todos as colunas
    # resultados podem ser restrigidos implementando a variável conditions
    # pode-se ordernar e estipular limite, atribuindo os valores para cada
    # variável
    def select(self, fields='*', conditions=None, order_by=None, limit=None):
        query = 'SELECT {} FROM {}'.format(fields, self.table)
        if conditions is not None:
            query += ' WHERE {}'.format(conditions)
        if order_by is not None:
            query += ' ORDER BY {}'.format(order_by)
        if limit is not None:
            query += ' LIMIT {}'.format(limit)
        self.last_query = query
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query)
                return cursor.fetchall()
            except err.MySQLError as error:
                return self.database_error(error)

    # funcão de update
    def update(self, new_values, column_value, column_to_search=None):
        if column_to_search is None:
            query = 'UPDATE {} SET {} WHERE {}={}'.format(self.table,
                                                          new_values,
                                                          self.primary_key,
                                                          column_value)
        else:
            query = query = 'UPDATE {} SET {} WHERE {}={}'.format(
                self.table, new_values, column_to_search, column_value)
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query)
                self.connection.commit()
                return True
            except err.MySQLError as error:
                self.connection.rollback()
                return self.database_error(error)

    # função de inserção. Só aceita dicionário como argumento. O dicionário
    # deve ser da seguinte forma {'coluna': 'valor'...}, sendo que 'coluna'
    # deve estar na lista self.fillable
    def create(self, values_dict):
        if not self.validate_fields(values_dict):
            _print.warning('Missing keys on {}.create() dictionary'
                           .format(self.table))
            return False
        query = 'INSERT INTO {} ({}) VALUES ({})'.format(
            self.table, self.get_concat_keys_from_dict(values_dict),
            self.get_concat_values_from_dict(values_dict))
        self.last_query = query
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query)
                self.connection.commit()
                return True
            except err.MySQLError as error:
                self.connection.rollback()
                return self.database_error(error)

    # função de deleção
    def delete(self, conditions):
        query = 'DELETE FROM {} WHERE {}'.format(self.table, conditions)
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query)
                self.connection.commit()
                return True
            except err.MySQLError as error:
                self.connection.rollback()
                return self.database_error(error)

    # retorna a primeira linha que satisfaça a condição
    def first(self, fields='*', conditions=None, order_by=None):
        result = self.select(fields, conditions, order_by, 1)
        return result[0] if result else False

    # retorna todas as linas que satisfaçam a condição passada
    def where(self, conditions, fields='*', order_by=None, limit=None):
        return self.select(fields, conditions, order_by, limit)

    # retorna a linha que satisfaça a condição passada, sendo que essa condição
    # é comparada à chave primária. Ou seja, retorna a primeira chave primaria
    # que satisfaça a condição
    def find(self, value, fields='*', conditions=None):
        final_condition = "{}='{}'".format(self.primary_key, value)
        if conditions is not None:
            final_condition += " AND {}".format(conditions)
        result = self.select(fields, final_condition)
        return result[0] if result else False

# -----------------------------------------------------------------------------
# FUNÇÕES AUXILIARES

    # retorna uma string concatenada dos valores de um dicionário
    def get_concat_values_from_dict(self, values_dict):
        return_string = ''
        for column in self.fillable:
            return_string += '"' + str(values_dict[column]) + '"' + ','
        return return_string[:-1]

    # retorna uma string concatenada das chaves de um dicionário
    def get_concat_keys_from_dict(self, values_dict):
        return_string = ''
        for column in self.fillable:
            return_string += column + ','
        return return_string[:-1]

    # verifica se as chaves presentes estão em self.fillable
    def validate_fields(self, fields):
        for required_field in self.fillable:
            if required_field not in fields:
                return False
        return True

# -----------------------------------------------------------------------------

    # mostra o erro causado, junto da função que causou o erro
    def database_error(self, error):
        _print.danger('Database error!')
        self.error_code = error.args[0]
        if env.DEBUG:
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            _print.warning('Error: {} in {}.{}'.format(
                str(error.args[1]), self.table, calframe[1][3]))
        return False
