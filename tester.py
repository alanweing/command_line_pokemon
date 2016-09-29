from model import Model

def main():
	test = Model('pokemons', ['name', 'category', 'rarity', 'ability', 'evolves_from', 'hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed'])
	print(test.select())


if __name__ == '__main__':
	main()