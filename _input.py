import _print


class Input:

    TYPE = 'type'
    MESSAGE = 'message'
    ACCEPTABLE = 'acceptable'
    LOOP = 'loop'

    INT    = 'integer'
    FLOAT  = 'float'
    STRING = 'string'

    _input = None
    _dict = None


    def get_input(self, _dict):
        self._dict = _dict
        if self.check_keys([self.TYPE, self.MESSAGE, self.ACCEPTABLE], self._dict):
            try:
                self._input = input(_print.question(str(_dict[self.MESSAGE])))
            except KeyboardInterrupt:
                _print.colorize('KeyboardInterrupt', color=_print.Color.RED, alert=True)
                exit(1)
            if self.LOOP in self._dict and self._dict[self.LOOP] == True and self._input == '':
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
            return True
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
                self._input = int(self._input)
            elif _type == self.FLOAT:
                self._input = float(self._input)
            elif _type == self.STRING:
                try:
                    self._input = int(self._input)
                except ValueError:
                    try:
                        self._input = float(self._input)
                    except ValueError:
                        self._input = str(self._input)
                    else:
                        _print.warning('Please, enter a valid value [%s].' % self._dict[self.TYPE])
                        self.get_input(self._dict)
                else:
                    _print.warning('Please, enter a valid value [%s].' % self._dict[self.TYPE])
                    self.get_input(self._dict)
        except ValueError:
            _print.warning('Please, enter a valid value [%s].' % self._dict[self.TYPE])
            self.get_input(self._dict)


    def validate_input(self):
        if self._dict[self.ACCEPTABLE] is None:
            return True
        return True if self._input in self._dict[self.ACCEPTABLE] else False
