import src.model as model
import src.data_base as data_base


class CozinhaPet():
    def __init__(self):
        self.recipes_DB = data_base.RecipesDB()
        self.ingredients_DB = data_base.IngredientsDB()

    #
    # Ingredients
    #

    def addIngredient(self,
                      name: str,
                      type: str,
                      unity: str,
                      price: str,
                      established: str,
                      amount: str = '1000',
                      cookingFactor: str = '1.',
                      safetyMargin: str = '1.') -> None:

        try:
            ingredient = model.Ingredient(name,
                                          type,
                                          unity,
                                          price,
                                          established,
                                          amount,
                                          cookingFactor,
                                          safetyMargin)
        except ValueError as err:
            raise(err)

        try:
            _id = self.ingredients_DB.addIngredient(ingredient)
        except RuntimeError as err:
            raise(err)
        except ValueError as err:
            raise(err)

        return _id

    def remIngredient(self, _id):
        try:
            self.ingredients_DB.removeIngredient(_id)
        except ValueError as err:
            raise(err)

    #
    # Recipes
    #

    def addRecipe(self,
                  pet: str,
                  tutor: str,
                  nutricionist: str,
                  recipeName: str) -> None:

        try:
            recipe = model.Recipe(pet, tutor, nutricionist, recipeName)
        except ValueError as err:
            raise(err)

        try:
            _id, registrationNumber = self.recipes_DB.addRecipe(recipe)
        except RuntimeError as err:
            raise(err)
        except ValueError as err:
            raise(err)

        return _id, registrationNumber

    def remRecipe(self, _id):
        try:
            self.recipes_DB.removeRecipe(_id)
        except ValueError as err:
            raise(err)

    #
    # Ingredients And Recipes
    #

    def updateIngredientsInRecipeFromDB(self, recipe_id):
        try:
            ingredientsList = self.recipes_DB.getIngredientsListFromRecipe(
                recipe_id)
        except ValueError as err:
            raise err

        raise ValueError(str(ingredientsList))

    def remIngredientFromRecipe(self, recipe_id, ingredient_id):
        try:
            self.recipes_DB.remIngredientFromRecipe(
                recipe_id, ingredient_id)
        except ValueError as err:
            raise err

    def addIngredientToRecipe(self, recipe_id, ingredient_id, dailyAmount):

        try:
            ingredient = self.ingredients_DB.getIngredientBy_id(ingredient_id)
            newestActualFactor = self.ingredients_DB.getNewestActualFactor(
                ingredient_id)

            ingredienteInRecipe = model.IngredientInRecipe(ingredient,
                                                           newestActualFactor,
                                                           dailyAmount)

            self.recipes_DB.addIngredientToRecipe(recipe_id,
                                                  ingredienteInRecipe)
        except ValueError as err:
            raise err
