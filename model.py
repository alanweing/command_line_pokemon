from database import MariaDB
from pymysql import connect, err
from functions import die
import inspect
import _print
import env

class Model(MariaDB):

    def __init__(self, table, fields):
        super().__init__()
        self.table = table
        self.fields = fields
        self.primary_key = 'id'
        self.fillable = []

    def __str__(self):
        return self.__dict__()
    #
    # def __repr__(self):
    #   pass
    #
    # def __del__(self):
    #   pass

    def select(self, fields='*', conditions=None, limit=None):
        query = 'SELECT {} FROM {}'.format(fields, self.table)
        if conditions is not None:
            query += ' WHERE {}'.format(conditions)
        if limit is not None:
            query += ' LIMIT {}'.format(limit)
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query)
                return self.parse_query_result(cursor.fetchall())
            except err.MySQLError as error:
                return self.database_error(error)

    def update(self):
        pass

    def create(self, values_dict):
        if not self.validate_fields(values_dict):
            _print.warning('Missing keys on {}.create() dictionary'.format(self.table))
            return False
        query = 'INSERT INTO {} ({}) VALUES ({})'.format(self.table, self.get_concat_keys_from_dict(values_dict), self.get_concat_values_from_dict(values_dict))
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query)
                self.connection.commit()
                return True
            except err.MySQLError as error:
                self.connection.rollback()
                return self.database_error(error)

    def delete(self):
        pass

    def first(self, fields='*', conditions=None):
        result =  self.select(fields, conditions, 1)
        return result[0] if result else False

    def where(self, conditions, fields='*', limit=None):
        return self.select(fields, conditions, limit)

    def find(self, value, fields='*'):
        result = self.select(fields, "{}='{}'".format(self.primary_key, value))
        return result[0] if result else False

#-------------------------------------------------------------------------------------------------------------------------

    def get_concat_values_from_dict(self, values_dict):
        return_string = ''
        for column in self.fillable:
            return_string += '`' + str(values_dict[column]) + '`' + ','
        return return_string[:-1]

    def get_concat_keys_from_dict(self, values_dict):
        return_string = ''
        for column in self.fillable:
            return_string += column + ','
        return return_string[:-1]

    def validate_fields(self, fields):
        for required_field in self.fillable:
            if required_field not in fields:
                return False
        return True

    def parse_query_result(self, query_result):
        return_object = []
        for row in query_result:
            _dict = {}
            for field in self.fields:
                _dict[field] = row[field]
            return_object.append(_dict)
        return return_object

#-------------------------------------------------------------------------------------------------------------------------

    def database_error(self, error):
        _print.danger('Database error!')
        if env.DEBUG:
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            _print.warning('Error: {} in {}.{}'.format(str(error.args[1]), self.table, calframe[1][3]))
        return False