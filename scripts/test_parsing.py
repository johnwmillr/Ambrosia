import json
import ambrosia

p = ambrosia.Parser()

recipes = [json.loads(str(line.rstrip('\n'))) for line in open('./ambrosia/data/full_format_recipes.json')]
recipes = recipes[0]

for n in range(100):
	print(recipes[n]['ingredients'])
	result = p.parseIngredients(recipes[n]['ingredients'])	
	for ingredient in result:
		print(ingredient)
	print(n)