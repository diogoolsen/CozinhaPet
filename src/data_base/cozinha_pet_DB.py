
from src.data_base.ingredients_DB import IngredientsDB
from src.data_base.recipes_DB import RecipesDB


class CozinhaPetDB(IngredientsDB, RecipesDB):
    #
    # FAZER NO DESING PATTERN
    #
    # Design Pattern Command
    #

    def convertIngredientTo_ingredientRecipe(self,
                                             ingredient_id_and_amount_tuple):

        _id, amount = ingredient_id_and_amount_tuple

        ingredient = self.getIngredientBy_id(_id)

        ingredientRecipe = {
            'name': ingredient['name'],
            'searchable': ingredient['searchable'],
            'type': ingredient['type'],      # meat, vegetable, supplement
            'unity': ingredient['unity'],           # g, ml, undefined (if supplement)
            'currentActualCookingFactor': self.getNewestActualFactor(_id),
            'establishedCostPer1K': ingredient['establishedCostPer1K'],
            'dailyAmount': amount
        }

        print('OK')
        return ingredientRecipe

    def addIngredientToRecipe(self,
                              recipe_id,
                              *ingredients_id_and_amount_tuples):

        for ingredient_id_and_amount_tuple in ingredients_id_and_amount_tuples:
            ing_rec = self.convertIngredientTo_ingredientRecipe(
                ingredient_id_and_amount_tuple)
            print(ing_rec)
