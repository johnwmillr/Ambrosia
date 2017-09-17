# Ambrosia
# Ahmed Elmaleh, John W. Miller, Qingyang Su
# See LICENSE for details
# 2017-09-16

"""A food library"""

from ingredients_parser.en import parse

# Parsing ingredient lists
import re
import nltk
from fractions import Fraction

from nltk.corpus import wordnet as wn

import ambrosia.parseIngredients as PI


class Ingredient(object):

    
    def __init__(self, name, amount='', units='', description=''):
        self._name = name # e.g. butter, sugar, etc. (this needs a better variable name than "name")        
        self._amount = amount # How many of units?
        self._units = units   # Measurement units (e.g. cup, tablespoon, pound, etc.)
        self._description = description # e.g. softened, blackened, etc.
                
    @property
    def name(self): # e.g. butter, chocolate chips, ground beef
        return self._name

    @property
    def units(self): # e.g. cups, teaspoons, oz
        return self._units
    
    @property
    def amount(self): # e.g. 1, 2, 1 1/2, 3/4
        return self._amount    
    
    @property
    def description(self): # e.g. softened, lightly-packed
        return self._description
    
    def __repr__(self):        
        return repr((self.amount, self.units, self.name))

class Parser(object):
    """Ambrosia Ingredient parser"""

    def __init__(self):
        data_loc="../data"

    def get_all_ingredients(self):
        food = wn.synset('food.n.02')
        foodList = list(set([w for s in food.closure(lambda s: s.hyponyms()) for w in s.lemma_names()]))
        foodList.sort();
        for ingredient in foodList:
            ingredient=ingredient.replace("_", " ")
        return foodList
    
    def parseIngredients(self, ingredients):
        """Take a list of ingredient strings and parse their values"""
        p = [parse(ingrd) for ingrd in ingredients]
        num_ingredients = len(p)

        # Use RegEx to get ingredient amount from parsed list
        expr = r'\d*\s*\d*((/|.|,)\d+)?'
        matches = [re.search(expr,ingrd['measure']) for ingrd in p]
        amounts = [match.group().strip().encode('ascii','ignore') for match in matches]            
        amounts = [a.replace(',','.') for a in amounts]        

        # Check for ill-formatted amounts (e.g. "1 /2")
        amt = []
        for a in amounts:
            m = re.search(r'\A\d?\s{1,3}/\d?',a)
            if m != None:                                
                amt.append(m.group().replace(' ',''))
            else:
                amt.append(a)
        amounts = amt
    
        # Convert amounts to float
        amounts = [float(sum(Fraction(s) for s in a.split())) for a in amounts]

        # Get measurement unit from the RegEx matches
        units = [i['measure'][m.end():].strip() for i,m in zip(p,matches)]

        # Use kbrokahn's parser method (which we modified)
        parsed_ingrds = PI.getIngredients(ingredients)
        names = [ingrd['ingredient'] for ingrd in parsed_ingrds]

        descriptions = [ingrd['descriptions'] for ingrd in parsed_ingrds]

        # Get parts of speech using NLTK
        # pos = [nltk.pos_tag(nltk.word_tokenize(ingrd['name'])) for ingrd in p]

        # Ingredient names
        # tags = ['NN','NNS','VBG'] #JJ also?
        # names = [' '.join([part[0] for part in parts if part[1] in tags]) for parts in pos]

        # Ingredient descriptions
        # tags = ['JJ','VBD']
        # descriptions = [' '.join([part[0] for part in parts if part[1] in tags]) for parts in pos]
                        
        return [Ingredient(n,a,u,d) for a,u,n,d in zip(amounts,units,names,descriptions)]




        


