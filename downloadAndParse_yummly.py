import sys
import re
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

def ingredientKludges(s):

    s = re.sub('^bananas$','banana',s)

    patterns = [
        '^t\s{1}', # "t honey"
        '\s?\d\/\d\scups?$', # "coffee 1/2 cup"
        '^\s*\d{1,2}-\d{1,2}\s?', # "1-2 dates"
        '\s*\d\%\s*(low-?\s?fat)?\s*', # "1% low fat milk"
        '\s*(\d\%)?\s?(low-?\s?fat)\s?', # "low fat milk"
        '^\d{1}/\d{1,2}-?\d{0,2}\s?', # "1/2-1 banana"
        'peeled'
        '(^c\.?\s?)|(^cups\s?)', # 'c coconut milk'
        '^c.',
        '^c\s{1}',
        '(^tbsp\s)|(^t\.?\s)', # 'tbsp honey'
        '(^tsp\s)', # 'tsp honey'
    ]

    s_in = s
    for ptr in patterns:        
        s = re.sub(ptr,'',s)        
        if s_in != s:
            print(s_in + ' --- ' + s + ' --- ' + ptr)
            s_in = s

    return s

def main(search_term, num_per_page=1, max_recipes=10):
    # default option values
    TIMEOUT = 5.0
    RETRIES = 0

    key, ID = load_credentials()

    client = Client(api_id=ID, api_key=key, timeout=TIMEOUT, retries=RETRIES)
    search = client.search(search_term)
    total_possible_matches = search.totalMatchCount

    page_num = 1
    num_matches, num_skips = 0,0
    allRecipes = pd.DataFrame()
    while num_matches < total_possible_matches and num_matches < max_recipes:
        search_results = client.search(search_term, maxResults=num_per_page, start=page_num)
        
        for match in search_results.matches:
            num_matches += 1
            current_ingredients = []
            try: # Due to dumb fraction errors        
                recipe = client.recipe(match.id)            
                data = parseIngredientList(recipe['ingredientLines'])
                quantities = []        
                for item in data:
                    assert item['name']!='', "An item needs a name."

                    # Divide by number of servings (if possible)
                    if item['qty'] != '' and isnumeric(recipe['numberOfServings']):
                        try:
                            # amount = float(Fraction(item['qty']))
                            amount = sum([float(Fraction(f)) for f in item['qty'].split()])
                            quantities.append(amount/recipe['numberOfServings'])
                            # amount = str(amount/recipe['numberOfServings']) + ' ' + item['unit']
                        except:
                            # quantities.append('unit')
                            quantities.append(1)
                    else:
                        # quantities.append('unit')
                        quantities.append(1)

                    item['name'] = item['name'].lower()

                    # Kludges
                    item['name'] = ingredientKludges(item['name'])

                    current_ingredients.append(item['name'])

                # Make a data frame from the current recipe
                DF = pd.DataFrame(np.array(quantities).reshape((1,len(current_ingredients))),columns=current_ingredients)        
                print('\n*************************\n' + recipe['name'])
                # print(DF)
                DF.insert(0,'Rating',recipe['rating'])
                DF.insert(0,'Title',recipe['name'])
                allRecipes = pd.concat([allRecipes,DF], axis=0, ignore_index=True)                

                # Continually wite to the .csv file
                allRecipes.to_csv("allRecipes.csv",mode='w',na_rep=0)
            except:
                print('\n-------------------------\n')
                print((sys.exc_info()[0], sys.exc_info()[1]))
                # print(data)
                # for item in data:
                    # print(item['input'])
                num_skips += 1
                # print('--------------------\n' + recipe['name'])

            if allRecipes.shape[0] > max_recipes:
                break
              
        page_num += num_per_page  
        print("\nYou downloaded {0} recipes in total and skipped {1}, i.e. {2} skip rate. You saved {3} recipes.".format(num_matches, num_skips, num_skips/float(num_matches),allRecipes.shape[0]))
                
def add_commas(*args):
    str_with_commas = args[0]
    for arg in args[1:]:
        str_with_commas = str_with_commas + ',' + str(arg)

    return str_with_commas

if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
    elif len(sys.argv) == 3:
        main(sys.argv[1],int(sys.argv[2]))
    else:
        main(sys.argv[1])