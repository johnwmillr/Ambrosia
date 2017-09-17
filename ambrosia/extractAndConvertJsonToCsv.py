# Extract the recipes.json data from here: https://github.com/kbrohkahn/recipe-parser

import json
import random
import math
import csv
import string

# Load in the huge json file as a list of many json objects
# recipes = [json.loads(str(line.rstrip('\n'))) for line in open('recipes.txt')] 

def extractUsefulRecipeData(recipes):    
    ingredientNames = []
    newObj = []        
    count = 0
    for recipe in recipes: # Iterate through all recipes        
        count += 1
        if count%100==0:
            print(count)

        recipeName = recipe['name'].replace(' ','_').encode('ascii', 'ignore').lower().translate(None, string.punctuation)
        tempObj = {'name': recipeName, 'ingredients': [], 'rating': math.ceil(10*random.random())}

        for ingredient in recipe['ingredients']: # Iterate through ingredients in current recipe                        
            d = {key: ingredient[key] for key in ingredient if key in ['amount','unit','ingredient']}                                        
            d['ingredient'] = d['ingredient'].encode('ascii', 'ignore').lower()
            tempObj['ingredients'].append(d)

            ingredientNames = ingredientNames + [d['ingredient']]
                        
        newObj = newObj + [tempObj]        

    return newObj, ingredientNames

def writeJsonToCsv(jsonObj, featureNames):    
    # Write the first row of the csv file
    featureNames.sort()
    featureNames.insert(0,'Rating')
    featureNames.insert(0,'RecipeName')    

    # Make a dictionary from the unique feature names
    d = {key: featureNames.index(key)+1 for key in featureNames}
    n_features = len(featureNames)

    with open("recipes_data.csv",'wb') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(featureNames)        
        for recipe in jsonObj:
            if count%100==0:
                print(count)
                
            recipeDataRow = [0]*(n_features+2)
            recipeDataRow[0] = recipe['name']
            recipeDataRow[1] = recipe['rating']

            for ingredient in recipe['ingredients']:
                recipeDataRow[d[ingredient['ingredient']]] = ingredient['amount']

            wr.writerow(recipeDataRow)

        