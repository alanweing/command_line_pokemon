from database import MariaDB
from pymysql import connect, err
import _print
import env

class Model(MariaDB):

    def __init__(self, table, fields):
        super().__init__()
        self.table = table
        self.fields = fields

    def __str__(self):
      pass

    def __repr__(self):
      pass

    def __del__(self):
      pass

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
                _print.danger('Database error!')
                if env.DEBUG:
                    _print.warning('Error: %s' % (str(error)))
                return False

    def update(self):
        pass

    def create(self):
        pass

    def parse_query_result(self, query_result):
        return_object = []
        for row in query_result:
            _dict = {}
            for field in self.fields:
                _dict[field] = row[field]
            return_object.append(_dict)
        return return_object


