from _input import Input
from controllers import PlayerController, PokemonController
from time import sleep
import _print
import env


class Terminator:

    # lista de comandos implementados
    available_commands = ['help', 'hunt', 'pokemon', 'exit', 'god_mode']

    def __init__(self):
        # classe auxiliar para o input
        self._input = Input()
        self.online = True
        # authorized diz se usuário já realizou login
        self.authorized = False
        # linhas mostrada no input
        self.line_input = '<#>:'
        # objeto que representa o usuário
        self.player = None
        # controladores de jogador e pokemon
        self.pokemon_controller = PokemonController()
        self.player_controller = PlayerController()
        _print.info('WELCOME TO POKEDEX!')

    def start(self):
        while self.online:
            # se o jogador ainda não tiver logado
            if self.authorized is False:
                _print.colorize('\t=>You can login or register in the system\
\n', _print.Color.RED)
                self._input.get(_print.question('What do you want to do?'),
                                'string', ['login', 'register'])
                if self._input.last_input == 'login':
                    login = self._input.get('login:', 'string', None)
                    password = self._input.get('password:', 'mixed', None)
                    # aqui o autorização é feita (método implementado no
                    # controlador)
                    if self.player_controller.authorize(login, password):
                        self.authorize_player(self.player_controller)
                    else:
                        _print.warning('Wrong credentials!')
                # registro do usuário
                elif self._input.last_input == 'register':
                    login = self._input.get('login:', 'string', None)
                    password = self._input.get('password:', 'mixed', None)
                    self.player_controller.create(login, password)
                    if self.player_controller.player.error_code is None:
                        self.authorize_player(self.player_controller)
                    elif self.player_controller.player.error_code == 1062:
                        _print.warning('this login ({}) is already in use!'
                                       .format(login))
                    else:
                        _print.danger('Whoops, something went wrong :( error \
code: {}'.format(self.player.error_code))

            # COMMANDS HANDLER
            else:
                # essa parte é executada toda vez que o usuário entrar com um
                # comando e estiver logado no sistema
                command = self._input.get(_print.question(self.line_input),
                                          'string', None).split(' ')
                if command[0] == '':
                    continue
                # verifica se o comando está na lista de comandos disponiveis
                if command[0] in Terminator.available_commands:
                    # comando de help lista todos os comandos disponívies
                    if command[0] == 'help':
                        _print.colorize('Available commands: {}'
                                        .format(Terminator.available_commands),
                                        _print.Color.BLUE)
                    # comando de caça
                    elif command[0] == 'hunt':
                        self.hunt()
                    elif command[0] == 'exit':
                        _print.info('Bye, {}!'
                                    .format(self.player_controller.login))
                        exit(0)
                    # pokemon pode ser listado, renomeado ou ordenado
                    elif command[0] == 'pokemon':
                        try:
                            if command[1] == 'list':
                                self.player_controller.list_pokemons()
                            elif command[1] == 'sort':
                                try:
                                    self.player_controller.order_pokemons(
                                        command[2])
                                except IndexError:
                                    _print.colorize('Usage: pokemon sort name|\
pokemon|type|rarity\nname and pokemon name are physically sorted\ntype and \
rarity are indirect arrays', _print.Color.RED)
                            elif command[1] == 'rename':
                                try:
                                    if command[2] == '':
                                        _print.colorize('Usage: pokemon rename\
 "pokemon name"', _print.Color.RED)
                                    self.player_controller.rename_pokemon(
                                        ' '.join(command[2:]))
                                except IndexError:
                                    _print.colorize('Usage: pokemon rename \
"pokemon name"', _print.Color.RED)
                            else:
                                _print.colorize('Usage: pokemon list|sort|\
                                rename', _print.Color.RED)
                        except IndexError:
                            _print.colorize('Usage: pokemon list|sort|rename',
                                            _print.Color.RED)
                    elif command[0] == 'god_mode':
                        self.player_controller.god_mode()
                else:
                    _print.colorize('Unknown command "{}", type "help" for \
more info'.format(command[0]), _print.Color.RED)

    # os dados do usuário são atualizados e line_input mostra o nome do usuário
    def authorize_player(self, player):
        self.authorized = True
        self.line_input = '<{}>:'.format(player.login)
        _print.success('You are now logged in!')

    # função que faz a caça pelo tempo necessário até encontrar um pokemon ou
    # um ovo
    def hunt(self):
        print('hunting!')
        pokemon = self.pokemon_controller.hunt()
        while pokemon is None:
            try:
                sleep(env.TIME_BETWEEN_HUNTING)
            except KeyboardInterrupt:
                exit(0)
            pokemon = self.pokemon_controller.hunt()
        if pokemon['name'] == 'Egg':
            _print.success("You've found an egg! It'll hatch \
in {} seconds".format(env.EGG_HATCH_TIME))
            self.player_controller.add_pokemon(pokemon['name'])
        elif len(self.player_controller.get_pokemons()) == 0:
            self.player_controller.add_pokemon(pokemon['name'])
            _print.success("You've found your first Pokemon!")
        else:
            _print.danger('Battle system not implemented!')
            _print.colorize("You've found:\n", _print.Color.GREEN, underline=True)
            for key, value in pokemon.items():
                print('\t{}: {}'.format(str(key).upper(), value))
            print('\n')
            opt = self._input.get('Do you want to collect this pokemon?', 'string', ['yes', 'y', 'no', 'n'])
            if opt == 'yes' or opt == 'y':
                self.player_controller.add_pokemon(pokemon['name'])
            # BATTLE SYSTEM
