
# from src.model.ingredient import Ingredient
# from src.data_base.ingredients_DB import IngredientsDB
# from src.data_base.recipes_DB import RecipesDB
# from src.data_base.cozinha_pet_DB import CozinhaPetDB


# DB = IngredientsDB()

# ingredient = Ingredient('Abóbora Paulista',
#                         'Vegetal',
#                         'g',
#                         '2',
#                         '2',
#                         cookingFactor='0.8',
#                         safetyMargin='1.03')

# try:
#     DB.addIngredient(ingredient.dict)
# except ValueError:
#     pass

# cursor = DB.getIngredientsCursorByNameSimilarity('abo')

# print('Busca por similaridade:')
# for ingredient in cursor:
#     # print(ingredient)
#     print('-- ' + ingredient.get('name'))

# print('\n')

# similarityList = DB.getIngredientsNamesListBySimilarity('abo')
# print('Lista de nomes similares:')
# print(similarityList)

# print('\n')

# id = DB.getIngredient_id('Abobrinha')
# print('Get _id:')
# print(id)

# # print('\n')
# # costItem = CostItem(31, 1000)
# # DB.addNewCost(id, costItem)

# print('\n')

# cost = DB.getNewestCost1K(id)
# print('Get Newest Cost 1K:')
# print(cost)

# print('\n')

# cost = DB.getNewestCost1Unity(id)
# print('Get Newest Cost 1Unity:')
# print(cost)

# # print('\n')
# # DB.addNewFactors(id, 0.90, 1.1)

# print('\n')

# factor = DB.getNewestCookingFactor(id)
# print('Get Newest Cooking Factor:')
# print(factor)

# print('\n')

# factor = DB.getNewestSafetyMargin(id)
# print('Get Newest Safety Margin:')
# print(factor)

# print('\n')

# factor = DB.getNewestActualFactor(id)
# print('Get Newest Actual Factor:')
# print(factor)


# #
# # Trabalhando com receitas
# #

# recipesDB = RecipesDB()

# # recipe = Recipe('Bruce', 'Marcela', 'Kássia', 'Bruce - Carne com Arroz')

# # recipesDB.addRecipe(recipe)

# cursor = recipesDB.getRecipeCursorByTermSimilarity('Ozzy tat')

# print('\n')

# print('Recipes:')
# for recipe_item in cursor:
#     print('\t' + recipe_item.get('petName') +
#           ' - ' + recipe_item.get('tutorName') +
#           ' - ' + recipe_item.get('recipeName'))

# # print(recipesDB.getAndIncrementRecipesCount())
