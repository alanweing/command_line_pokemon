from _input import Input
from threading import Thread
from controllers import PlayerController, PokemonController
import _print
import views
from time import sleep

class Terminator:

	available_commands = ['help', 'hunt']

	def __init__(self):
		self._input = Input()
		self.online = True
		self.authorized = False
		self.line_input = '<#>:'
		views.welcome()
		Thread(target=self.get_command()).start()
		self.pokemon_controller = PokemonController()

	def get_command(self):
		while self.online:
			if self.authorized is False:
				_print.colorize('\t=>You can signin or signup in the system\n', _print.Color.RED)
				self._input.get(_print.question('What do you want to do?'), 'string', ['signin', 'signup'])
				if self._input.last_input == 'signin':
					login = self._input.get('login:', 'string', None)
					password = self._input.get('password:', 'mixed', None)
					player, authorized = PlayerController.authorize(login, password)
					if authorized is not False:
						self.authorize_player(player)
					else:
						_print.warning('Wrong credentials!')
				elif self._input.last_input == 'signup':
					login = self._input.get('login:', 'string', None)
					password = self._input.get('password:', 'mixed', None)
					new_player = PlayerController.create(login, password)
					if new_player.error_code is None:
						self.authorize_player(new_player)
					elif new_player.error_code == 1062:
						_print.warning('this login ({}) is already in use!'.format(login))
					else:
						_print.danger('Whoops, something went wrong :( error code: {}'.format(new_player.error_code))

			else:
				command = self._input.get(_print.question(self.line_input), 'string', None)
				if command in Terminator.available_commands:
					if command == 'help':
						_print.colorize('Available commands: {}'.format(Terminator.available_commands), _print.Color.BLUE)
					elif command == 'hunt':
						print('hunting!')
						pokemon = self.pokemon_controller.hunt()
						while pokemon is None:
							print('.', end='')
							sleep(.3)
							pokemon = self.pokemon_controller.hunt()
						print('found:', pokemon)

				else:
					_print.colorize('Unknown command "{}", type "help" for more info'.format(command), _print.Color.RED)

	def authorize_player(self, player):
		self.player = player
		self.authorized = True
		self.line_input = '<{}>:'.format(player.login)
		_print.success('You are now logged in!')	