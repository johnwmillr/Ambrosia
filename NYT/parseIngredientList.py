# coding=utf8
from __future__ import print_function

import sys
import os
import tempfile
import json
import re

from ingredient_phrase_tagger.training import utils

from ambrosia.parser import Parser
P = Parser()

def parseIngredientList(ingredients):
    """ingredients is a list of ingredients and descriptions from a recipe"""

    try:    
        # Flour kludge
        for i, item in enumerate(ingredients):
            ingredients[i] = re.sub('all purpose','all-purpose',item)

        # 1/3 amount kludge (weird NYT bug)
        firstParse = P.parseIngredients(ingredients)
        one_thirds = []
        for i,item in enumerate(firstParse):
            if item.amount==1/3.0:
                one_thirds.append(i)
        
        # Write the list of ingredients to a file
        ingredientFile = "./NYT/ingredients.txt"
        with open(ingredientFile,'w') as outfile:
            for item in ingredients:
                # Unicode kludge
                line = str(item.encode("utf-8", errors='ignore').decode("utf-8") + "\n")
                line = line.replace('½', ' 0.5').strip(' ')
                line = line.replace('⅓', ' 1/3').strip(' ')            
                line = line.replace('⅔', ' 2/3').strip(' ')
                line = line.replace('¼', ' 0.25').strip(' ')            
                line = line.replace('¾', ' 0.75').strip(' ')                        
                # print(line)
                outfile.writelines(line)

        # Use the trained model to predict tags for the list of ingredients
        result = os.system("python ./NYT/bin/parse-ingredients.py ./NYT/ingredients.txt > ./NYT/results.txt")
        if result != 0:
            print('System error. Error code: {0}'.format(result))
            
        # Convert result to json format
        result = os.system("python ./NYT/bin/convert-to-json.py ./NYT/results.txt > ./NYT/results.json")
        if result != 0:
            print('System error. Error code: {0}'.format(result))
            
        # Return the json format
        json_obj = json.load(open('./NYT/results.json'))

        # Kludge to fix 1/3 in NYT
        for i, item in enumerate(json_obj):
            if i in one_thirds:
                json_obj[i]['qty'] = '1/3'
    except:
        print(sys.exc_info()[0])
        json_obj = []

    return json_obj