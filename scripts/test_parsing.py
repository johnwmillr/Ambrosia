import json
import ambrosia

p = ambrosia.Parser()

recipes = [json.loads(str(line.rstrip('\n'))) for line in open('./ambrosia/data/full_format_recipes.json')]
recipes = recipes[0]

for n in range(15000,len(recipes)):		
	if 'ingredients' in recipes[n].keys():
		result = p.parseIngredients(recipes[n]['ingredients'])
		if n%100==0 or n==0:
			print(result)
			print(n)			
			print('')
		
	
		