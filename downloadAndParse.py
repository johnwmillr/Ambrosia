import sys
import ambrosia
from NYT.parseIngredientList import parseIngredientList

api = ambrosia.API()


def main(search_term, num=1):
    recipes = api.search(search_term,count=num)

    filename = 'parsed_ingredients.txt'

    all_ingredients = []

    with open(filename,'w') as outfile:
        for recipe in recipes:
            print('\n*************************\n' + recipe['title'])
            outfile.write('\n')
            data = parseIngredientList(recipe['ingredients'])

            for item in data:
                row = add_commas(recipe['title'],recipe['social_rank'],item['qty'],item['unit'],item['name'])
                outfile.write(row+'\n')
                # print(row+'\n')

                if item['name'] not in all_ingredients:            
                    all_ingredients.append(item['name'])

            parsedIngredients = [(item['qty'], item['unit'], item['name']) for item in data]            
            for i,item in enumerate(parsedIngredients):
                print('\n' + str(data[i]['input']) + ' --- ' + str(item))

    all_ingredients.sort()
    for item in all_ingredients:
        print(str(item) + '\n')


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