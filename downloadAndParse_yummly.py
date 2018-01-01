import sys
from fractions import Fraction
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

def main(search_term, num=1):
    # default option values
    TIMEOUT = 5.0
    RETRIES = 0

    key, ID = load_credentials()

    client = Client(api_id=ID, api_key=key, timeout=TIMEOUT, retries=RETRIES)
    search = client.search(search_term)#, maxResults=num)#, start=1)

    filename = 'parsed_ingredients.txt'
    all_ingredients = []

    with open(filename,'w') as outfile:
        # for recipe in recipes:
        for match in search.matches:
            try:
                recipe = client.recipe(match.id)            
                print('\n*************************\n' + recipe['name'])
                outfile.write('\n')
                data = parseIngredientList(recipe['ingredientLines'])

                row1, row2 = '',''
                for item in data:
                    row1 = row1 + item['name'] + ','
                    # try:
                    amount = float(Fraction(item['qty']))
                    row2 = row2 + str(amount/recipe['numberOfServings']) + ' ' + item['unit'] + ','
                    # except:
                        # row2 = row2 + item['qty'] + ' ' + item['unit'] + ','

                print(row1)
                print(row2)
                outfile.write(row1+'\n')
                outfile.write(row2+'\n')
            except:
                pass

            # for item in data:
            #     row = add_commas(recipe['name'],recipe['rating'],item['qty'],item['unit'],item['name'])
            #     outfile.write(row+'\n')
            #     # print(row+'\n')

            #     if item['name'] not in all_ingredients:            
            #         all_ingredients.append(item['name'])

            # parsedIngredients = [(item['qty'], item['unit'], item['name']) for item in data]            
            # for i,item in enumerate(parsedIngredients):
            #     print('\n' + str(data[i]['input']) + ' --- ' + str(item))

    # all_ingredients.sort()
    # for item in all_ingredients:
    #     print(str(item) + '\n')


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