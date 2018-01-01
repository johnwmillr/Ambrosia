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

def replaceFractions(s):
    s_in = s

    FRACTIONS = {
    u'½': u' 1/2',
    u'⅓': u' 1/3', 
    u'⅔': u' 2/3', 
    u'¼': u' 1/4', 
    u'¾': u' 3/4', 
    u'⅕': u' 1/5', 
    u'⅖': u' 2/5', 
    u'⅗': u' 3/5', 
    u'⅘': u' 4/5', 
    u'⅙': u' 1/6', 
    u'⅚': u' 5/6', 
    u'⅐': u' 1/7',
    u'⅛': u' 1/8', 
    u'⅜': u' 3/8', 
    u'⅝': u' 5/8', 
    u'⅞': u' 7/8', 
    u'⅑': u' 1/9',
    u'⅒': u' 1/10'
    }

    for k in FRACTIONS:
        if k in s:
            s = s.replace(k, FRACTIONS[k]).strip(' ')

    return s

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
                item = replaceFractions(item)
                line = str(item.encode("utf-8", errors='ignore').decode("utf-8") + "\n")
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
        print((sys.exc_info()[0], sys.exc_info()[1]))
        json_obj = []

    return json_obj