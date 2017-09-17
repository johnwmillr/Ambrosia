from collections import Counter

def freq_dist(allIngredients):
    # Replace ingredients with more frequently used similar terms
    counts = Counter(allIngredients)

    parsedIngredients = []
    oldToNewPairs = {}
    for ingredient in allIngredients:
        max_freq = 0
        new_ingrd = []
        for word in ingredient.split():
            if max_freq > 0 and counts[word] == max_freq:
                new_ingrd = new_ingrd + ' ' + word
            elif counts[word] > max_freq and counts[word] >= counts[ingredient]:
                max_freq = counts[word]
                new_ingrd = word                        
        
        if new_ingrd == []:
            new_ingrd = ingredient

        oldToNewPairs[ingredient] = new_ingrd
        parsedIngredients.append(new_ingrd)
        # print((ingredient, new_ingrd, max_freq))

    return counts, parsedIngredients, oldToNewPairs

def freq_dist2(allIngredients):
    # Only keep the most frequently used ingredients
    u = Counter(allIngredients)
    parsedIngredients = [un for un in u if u[un]>5]
    
    return u, parsedIngredients

def changeIngredientNamesInDict(recipes, mapping):
    newDict = []
    count = 0    
    for recipe in recipes:
        i = 0
        newDict[count] = recipe
        for ingredient in recipe['ingredients']:
            if ingredient['name'] in mapping.keys():
                newName = mapping[ingredient['name']]                        
            else:
                newName = ingredient['name']
                
            newDict[count]['ingredients'][i] = ingredient
            newDict[count]['ingredients'][i]['name'] = newName
            i+=1

        count += 1

        if count%100==0:
            print(count)

    return newDict