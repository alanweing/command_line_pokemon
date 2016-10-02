from _input import Input
from threading import Thread
from controllers import PlayerController, PokemonController
from time import sleep
from functions import die
import _print
import views
import env

class Terminator:

    available_commands = ['help', 'hunt']

    def __init__(self):
        self._input = Input()
        self.online = True
        self.authorized = False
        self.line_input = '<#>:'
        self.player = None
        views.welcome()
        self.pokemon_controller = PokemonController()
        self.player_controller = PlayerController()

    def start(self):
        while self.online:
            if self.authorized is False:
                _print.colorize('\t=>You can signin or signup in the system\n', _print.Color.RED)
                self._input.get(_print.question('What do you want to do?'), 'string', ['signin', 'signup'])
                if self._input.last_input == 'signin':
                    login = self._input.get('login:', 'string', None)
                    password = self._input.get('password:', 'mixed', None)
                    if self.player_controller.authorize(login, password):
                        self.authorize_player(self.player_controller)
                    else:
                        _print.warning('Wrong credentials!')
                elif self._input.last_input == 'signup':
                    login = self._input.get('login:', 'string', None)
                    password = self._input.get('password:', 'mixed', None)
                    self.player_controller.create(login, password)
                    if self.player_controller.player.error_code is None:
                        self.authorize_player(self.player_controller)
                    elif self.player_controller.player.error_code == 1062:
                        _print.warning('this login ({}) is already in use!'.format(login))
                    else:
                        _print.danger('Whoops, something went wrong :( error code: {}'.format(new_player.error_code))

            # COMMANDS HANDLER
            else:
                command = self._input.get(_print.question(self.line_input), 'string', None)
                if command in Terminator.available_commands:
                    if command == 'help':
                        _print.colorize('Available commands: {}'.format(Terminator.available_commands), _print.Color.BLUE)
                    elif command == 'hunt':
                        self.hunt()
                else:
                    _print.colorize('Unknown command "{}", type "help" for more info'.format(command), _print.Color.RED)

    def authorize_player(self, player):
        self.authorized = True
        self.line_input = '<{}>:'.format(player.login)
        _print.success('You are now logged in!')

    def hunt(self):
        print('hunting!')
        pokemon = self.pokemon_controller.hunt()
        while pokemon is None:
            try:
                sleep(env.TIME_BETWEEN_HUNTING)
            except KeyboardInterrupt:
                exit(0)
            pokemon = self.pokemon_controller.hunt()
        if len(self.player_controller.pokemons()) == 0:
            self.player_controller.add_pokemon(self.player.login, pokemon['name'])
            _print.success("Congratulations! You've found your first Pokemon!")
            print('found:', pokemon)
        else:
            _print.danger('BATTLE, MOTHERFUCKER!')
