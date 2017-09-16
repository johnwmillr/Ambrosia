import ambrosia

p = ambrosia.Parser()

ingredients = [u'2 cups all-purpose flour',
 u'2 1/2 cups sugar',
 u'3/4 cup unsweetened cocoa powder, preferably Dutch process',
 u'2 teaspoons baking soda',
 u'1 teaspoon salt',
 u'1 cup neutral vegetable oil, such as canola, soybean or vegetable blend',
 u'1 cup sour cream',
 u'1 1/2 cups water',
 u'2 tablespoons distilled white vinegar',
 u'1 teaspoon vanilla extract',
 u'2 eggs',
 u'1/2 cup coarsely chopped peanut brittle (I skipped this)',
 u'10 ounces cream cheese, at room temperature',
 u'1 stick (4 ounces) unsalted butter, at room temperature',
 u'5 cups confectioners sugar, sifted',
 u'2/3 cup smooth peanut butter, preferably a commercial brand (because oil doesnt separate out)',
 u'8 ounces semisweet chocolate, coarsely chopped',
 u'3 tablespoons smooth peanut butter',
 u'2 tablespoons light corn syrup',
 u'1/2 cup half-and-half']

parsed_ingrds = p.parseIngredients(ingredients)

for ingrd in parsed_ingrds:
	print(ingrd)