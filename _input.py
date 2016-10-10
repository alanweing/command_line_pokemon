import _print


class Input:

    # Chaves para utilizar durante a criação do dicionário
    TYPE = 'type'
    MESSAGE = 'message'
    ACCEPTABLE = 'acceptable'
    LOOP = 'loop'

    # Chaves que asseguram a integridade do input
    INT = 'integer'
    FLOAT = 'float'
    STRING = 'string'
    MIXED = 'mixed'

    last_input = None
    _dict = None

    def get_input(self, _dict):
        self._dict = _dict
        # verifica se todas as chaves essenciais estão presentes em _dict
        if self.check_keys([self.TYPE, self.MESSAGE, self.ACCEPTABLE],
                           self._dict):
            try:
                # armazena o último input do usuário para uso futuro, se
                # necessário
                self.last_input = input(_print.question(
                    str(_dict[self.MESSAGE])))
            # tratamento de erro para uma interrupção
            except KeyboardInterrupt:
                _print.colorize('KeyboardInterrupt', color=_print.Color.RED,
                                alert=True)
                exit(1)
            # se a chave loop for definida como verdadeira e o usuário
            # pressionar enter duas vezes, quebra o loop
            if self.LOOP in self._dict and self._dict[self.LOOP] is True and\
                    self.last_input == '':
                return False
            # valida o input do usuário
            self.cast_input()
            # se o input não estiver dentro dos valores aceitáveis
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

    # método que valida as chaves dentro do dicionário recebido
    @staticmethod
    def check_keys(keys, _dict):
        for key in keys:
            if key not in _dict:
                return False
        return True

    # função responsável por assegurar que o valor digitado é o esperado
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

    # faz a validação do input, isto é, retorna verdadeiro se o valor é
    # aceitável, falso caso não
    def validate_input(self):
        if self._dict[self.ACCEPTABLE] is None:
            return True
        return True if self.last_input in self._dict[self.ACCEPTABLE] \
            else False

    # função para montar o dicionário a ser enviado ao _input. Ter que montar
    # esse mesmo dicionário toda vez que fosse necessário um input se torna
    # inviável
    def get(self, message, _type, acceptable, loop=False):
        return self.get_input({
            self.TYPE: _type,
            self.MESSAGE: message,
            self.ACCEPTABLE: acceptable,
            self.LOOP: loop})


# exemplos de uso para o get_input; abaixo de cada exemplo é usado a função
# get que faz a mesma coisa de forma mais simples:
# Input().get_input({
#     'type': 'string',
#     'message': 'Digite um texto:',
#     'acceptable': ['texto', 'aceitável'],
#     'loop': True  # dois 'enters' quebram o loop (retorna False)
# })
# Input().get('string', 'Digite um texto', ['text', 'aceitável'], True)
#
# Input().get_input({
#     'type': 'int',
#     'message': 'Entre com um inteiro:',
#     'acceptable': [1, 2, 3, 4],
# })
# Input().get('int', 'Entre com um inteiro', [1, 2, 3, 4])
#
# Input().get_input({
#     'type': 'string',
#     'message': 'Digite um texto:',
#     'acceptable': None,  # aceita qualquer valor
# })
# Input().get('string', 'Digite um texto:', None)
#
# Input().get_input({
#     'type': 'mixed',  # inteiro e string
#     'message': 'Digite um valor misto:',
#     'acceptable': None,
# })
# Input().get('mixed', 'Digite um valor misto', None)
