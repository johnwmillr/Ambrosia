import json
import ambrosia
from collections import Counter

from ambrosia.extractAndConvertJsonToCsv import extractUsefulRecipeData, writeJsonToCsv

Recipes = [json.loads(str(line.rstrip('\n'))) for line in open('./ambrosia/data/full_format_recipes.json')]
Recipes = Recipes[0]

def getTheThings():
	recipes, allIngredients, allRatings = extractUsefulRecipeData(Recipes)

	return recipes, allIngredients, allRatings

# counts_ingredients = Counter(allIngredients)