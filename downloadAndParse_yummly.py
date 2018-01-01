import sys
from fractions import Fraction
import pandas as pd
import numpy as np
# import ambrosia
from NYT.parseIngredientList import parseIngredientList
from ambrosia import yummly
from yummly import Client

# api = ambrosia.API()

def load_credentials():
    """Load the Yummly.com API credentials"""
    lines = [str(line.rstrip('\n')) for line in open('secrets.txt')]
    for line in lines:
        if "api_key_yummly" in line:
            api_key = line.split(": ")[1]
        if "api_id_yummly" in line:
            api_id = line.split(": ")[1]

    return api_key, api_id

def isnumeric(val):
    if isinstance(val, int) or isinstance(val, float):
        return True
    else:
        return False

def main(search_term, num=1):
    # default option values
    TIMEOUT = 5.0
    RETRIES = 0

    key, ID = load_credentials()

    client = Client(api_id=ID, api_key=key, timeout=TIMEOUT, retries=RETRIES)
    search = client.search(search_term)#, maxResults=num)#, start=1)

    allRecipes = pd.DataFrame()
    num_matches,num_skips = 0,0
    for match in search.matches:
        num_matches += 1
        try:
            current_ingredients = []
            recipe = client.recipe(match.id)
            print('\n*************************\n' + recipe['name'])
            data = parseIngredientList(recipe['ingredientLines'])

            quantities = []
            for item in data:
                assert item['name']!='', "An item needs a name."

                # Divide by number of servings (if possible)
                if item['qty'] != '' and isnumeric(recipe['numberOfServings']):
                    amount = float(Fraction(item['qty']))
                    quantities.append(amount/recipe['numberOfServings'])
                    amount = str(amount/recipe['numberOfServings']) + ' ' + item['unit']
                else:
                    quantities.append('unit')

                item['name'] = item['name'].lower()
                current_ingredients.append(item['name'])

            # Make a data frame from the current recipe
            DF = pd.DataFrame(np.array(quantities).reshape((1,len(current_ingredients))),columns=current_ingredients)
            print(quantities)
            print(current_ingredients)
            print(DF)                
            allRecipes = pd.concat([allRecipes,DF], axis=0, ignore_index=True)                
        except:
            num_skips += 1
            
        # Continually wite to the .csv file
        allRecipes.to_csv("allRecipes.csv",mode='w',na_rep=0)

    print("\nYou downloaded {0} recipes in total and skipped {1}, i.e. {2} skip rate.".format(num_matches, num_skips, num_skips/float(num_matches)))
    
def add_commas(*args):
    str_with_commas = args[0]
    for arg in args[1:]:
        str_with_commas = str_with_commas + ',' + str(arg)

    return str_with_commas

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1],int(sys.argv[2]))
    else:
        main(sys.argv[1])