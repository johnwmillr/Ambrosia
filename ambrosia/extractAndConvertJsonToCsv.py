# Extract the recipes.json data from here: https://github.com/kbrohkahn/recipe-parser

import json
import math
import csv
import string
import urllib2
import re
from bs4 import BeautifulSoup

import ambrosia.parser
parser = ambrosia.Parser()

# Load in the huge json file as a list of many json objects
# recipes = [json.loads(str(line.rstrip('\n'))) for line in open('recipes.txt')] 

def getAllRecipesRating(recipe_id):
    url = "http://allrecipes.com/recipe/" + str(recipe_id)
    soup = BeautifulSoup(urllib2.urlopen(url).read(),'lxml')
    html_snippet = str(soup.find("section",{"class":"recipe-summary clearfix"}).find("meta"))    
    rating = float(re.search('="\d\.\d*"',html_snippet).group().split('"')[1])
    
    return rating

def extractUsefulRecipeData(recipes):    
    newObj, allIngredients, allRatings = [],[],[]
    count = 0; print(count)
    for recipe in recipes: # Iterate through all recipes        
        count += 1
        if count%100==0:
            print(count)

        # Get the recipe rating        
        # rating = getAllRecipesRating(recipe['id'])                
        if 'rating' in recipe.keys() and 'title' in recipe.keys():
            rating = recipe['rating']
            allRatings.append(rating)

            # recipeName = recipe['name'].replace(' ','_').encode('ascii', 'ignore').lower().translate(None, string.punctuation)
            recipeName = recipe['title'].replace(' ','_').encode('ascii', 'ignore').lower().translate(None, string.punctuation)
            tempObj = {'name': recipeName, 'ingredients': [], 'rating': rating}

            ingredients = parser.parseIngredients(recipe['ingredients'])

            for ingredient in ingredients: # Iterate through ingredients in current recipe                                    
                # d = {key: ingredient[key] for key in ingredient if key in ['amount','unit','ingredient']}                                        
                d = {'amount':ingredient.amount, 'unit':ingredient.units, 'name':ingredient.name}            
                d['name'] = d['name'].encode('ascii', 'ignore').lower()
                tempObj['ingredients'].append(d)

                allIngredients = allIngredients + [d['name']]
                        
            newObj = newObj + [tempObj]
        else:
            print('missing')

    # Normalize the ratings    
    for n in range(len(allRatings)):
        if allRatings[n] == None:
            allRatings[n] = 0 

    allRatings = [10*((float(i)-min(allRatings))/(max(allRatings)-min(allRatings))) for i in allRatings]

    # Only keep the unique ingredient names
    # allIngredients = list(set(allIngredients))


    return newObj, allIngredients, allRatings


def writeJsonToCsv(jsonObj, featureNames):    
    # Write the first row of the csv file
    featureNames.sort()
    featureNames.insert(0,'Rating')
    featureNames.insert(0,'RecipeName')    

    # Make a dictionary from the unique feature names
    d = {key: featureNames.index(key)+1 for key in featureNames}
    n_features = len(featureNames)    

    count = 0    
    with open("recipes_data_trimmed_features.csv",'wb') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(featureNames)        
        for n in jsonObj:
            recipe = jsonObj[n]

            if count%100==0 or count==0:
                print(count)
                
            recipeDataRow = [0]*(n_features+2)            
            recipeDataRow[0] = recipe['name']
            recipeDataRow[1] = recipe['rating']

            for ingredient in recipe['ingredients']:
                recipeDataRow[d[ingredient['name']]] = ingredient['amount']

            wr.writerow(recipeDataRow)
            count += 1
            if count%100==0:
                print(count)

        