__author__ = 'sheraz/nibesh'

import re
from itertools import chain

from utils import normalize, escape_re_string

UNITS = {"cup": ["cups", "cup", "c.", "c"], "fluid_ounce": ["fl. oz.", "fl oz", "fluid ounce", "fluid oz", "fluid ounces"],
         "gallon": ["gal", "gal.", "gallon", "gallons"], "ounce": ["oz", "oz.", "ounce", "ounces"],
         "pint": ["pt", "pt.", "pint", "pints"], "pound": ["lb", "lb.", "pound", "pounds"],
         "quart": ["qt", "qt.", "qts", "qts.", "quart", "quarts"],
         "tablespoon": ["tbsp.", "tbsp", "T", "T.", "tablespoon", "tablespoons", "tbs.", "tbs"],
         "teaspoon": ["tsp.", "tsp", "t", "t.", "teaspoon", "teaspoons"],
         "gram": ["g", "g.", "gr", "gr.", "gram", "grams"], "kilogram": ["kg", "kg.", "kilogram", "kilograms"],
         "liter": ["l", "l.", "liter", "liters"], "milligram": ["mg", "mg.", "milligram", "milligrams"],
         "milliliter": ["ml", "ml.", "milliliter", "milliliters"], "pinch": ["pinch", "pinches"],
         "dash": ["dash", "dashes"], "touch": ["touch", "touches"], "handful": ["handful", "handfuls"],
         "stick": ["stick", "sticks"], "clove": ["cloves", "clove"], "can": ["cans", "can"],"slice":["slice","slices"],
         "large": ["large","whole large"], "medium": ["medium"], "small": ["small"], "scoop": ["scoop", "scoops"],
         "filets": ["filet", "filets"],"sprig": ["sprigs", "sprig"],"whole": ["whole"],"splash": ['splash','splashes']}

NUMBERS = ['seventeen', 'eighteen', 'thirteen', 'nineteen', 'fourteen', 'sixteen', 'fifteen', 'seventy', 'twelve',
           'eleven', 'eighty', 'thirty', 'ninety', 'twenty', 'seven', 'fifty', 'sixty', 'forty', 'three', 'eight',
           'four', 'zero', 'five', 'nine', 'ten', 'one', 'six', 'two', 'an', 'a']

prepositions = ["of"]

a = list(chain.from_iterable(UNITS.values()))
a.sort(key=lambda x: len(x), reverse=True)
a = map(escape_re_string, a)

PARSER_RE = re.compile(
    r'(?P<quantity>(?:[\d\.,][\d\.,\s/]*)?\s*(?:(?:%s)\s*)*)?(\s*(?P<unit>%s)\s+)?(\s*(?:%s)\s+)?(\s*(?P<name>.+))?' % (
        '|'.join(NUMBERS), '|'.join(a), '|'.join(prepositions)))

def parse(st):
    """

    :param st:
    :return:
    """
    st = normalize(st.lower())
    res = PARSER_RE.match(st)
        
    # Replace unit variation with standard unit key (e.g. fl. oz. becomes fluid_ounce)
    try:
        unit = [key for key, vals in UNITS.iteritems() if res.group('unit') in vals][0]
    except:
        unit = ''

    # TODO: Add option to handle the "1 (7.5 oz) can of tomato" scenario

    return {
        'measure': ((res.group('quantity') or '').strip() + ' ' + (unit or '').strip()).strip(),
        'name': (res.group('name') or '').strip()
    }