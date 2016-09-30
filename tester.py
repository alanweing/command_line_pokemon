# from model import Model
#
# def main():
#     test = Model('pokemons', ['name', 'category', 'rarity', 'ability', 'evolves_from', 'hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed'])
#     # test.primary_key = 'name'
#     # print(test.first())
#     # print(test.find('Arbok'))
#     test.fillable = ['name', 'category', 'rarity']
#     test.create({'name': 'nome', 'category':'categoria', 'rarity': 'raridade'})
#
#
# if __name__ == '__main__':
# 	main()

from controllers import PlayerController

player = PlayerController.create('teste', '123456')
print(player)
