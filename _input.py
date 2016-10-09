import _print


class Input:

    TYPE = 'type'
    MESSAGE = 'message'
    ACCEPTABLE = 'acceptable'
    LOOP = 'loop'

    INT = 'integer'
    FLOAT = 'float'
    STRING = 'string'
    MIXED = 'mixed'

    last_input = None
    _dict = None

    def get_input(self, _dict):
        self._dict = _dict
        if self.check_keys([self.TYPE, self.MESSAGE, self.ACCEPTABLE],
                           self._dict):
            try:
                self.last_input = input(_print.question(
                    str(_dict[self.MESSAGE])))
            except KeyboardInterrupt:
                _print.colorize('KeyboardInterrupt', color=_print.Color.RED,
                                alert=True)
                exit(1)
            if self.LOOP in self._dict and self._dict[self.LOOP] is True and\
                    self.last_input == '':
                return False
            self.cast_input()
            if not self.validate_input():
                if self._dict[self.ACCEPTABLE] is None:
                    _print.warning('Enter a value!')
                else:
                    _print.warning('This is not a valid value!')
                    values = ''
                    for value in self._dict[self.ACCEPTABLE]:
                        values += str(value) + '|'
                    values = values[:-1]
                    _print.info('Acceptable values: [%s]' % values)
                self.get_input(self._dict)
            return self.last_input
        else:
            _print.danger('Missing keys!')
            return False

    @staticmethod
    def check_keys(keys, _dict):
        for key in keys:
            if key not in _dict:
                return False
        return True

    def cast_input(self):
        try:
            _type = self._dict[self.TYPE]
            if _type == self.INT:
                self.last_input = int(self.last_input)
            elif _type == self.FLOAT:
                self.last_input = float(self.last_input)
            elif _type == self.MIXED:
                self.last_input = str(self.last_input)
            elif _type == self.STRING:
                try:
                    self.last_input = int(self.last_input)
                except ValueError:
                    try:
                        self.last_input = float(self.last_input)
                    except ValueError:
                        self.last_input = str(self.last_input)
                    else:
                        _print.warning('Please, enter a valid value [%s].' %
                                       self._dict[self.TYPE])
                        self.get_input(self._dict)
                else:
                    _print.warning('Please, enter a valid value [%s].' %
                                   self._dict[self.TYPE])
                    self.get_input(self._dict)
        except ValueError:
            _print.warning('Please, enter a valid value [%s].' %
                           self._dict[self.TYPE])
            self.get_input(self._dict)

    def validate_input(self):
        if self._dict[self.ACCEPTABLE] is None:
            return True
        return True if self.last_input in self._dict[self.ACCEPTABLE] \
            else False

    def get(self, message, _type, acceptable, loop=False):
        return self.get_input({
            self.TYPE: _type,
            self.MESSAGE: message,
            self.ACCEPTABLE: acceptable,
            self.LOOP: loop})
