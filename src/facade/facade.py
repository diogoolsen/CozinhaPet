import src.model as Model

from src.data_base.recipes_DB import RecipesDB


class Facade():
    def __init__(self, recipes_DB, ingredients_DB):
        self.recipes_DB = recipes_DB
        self.ingredients_DB = ingredients_DB

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
            ingredient = Model.Ingredient(name,
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
            self.ingredients_DB.addIngredient(ingredient)
        except RuntimeError as err:
            raise(err)
        except ValueError as err:
            raise(err)

    def addRecipe(self,
                  recipeDB: RecipesDB,
                  pet: str,
                  tutor: str,
                  nutricionist: str,
                  recipeName: str) -> None:

        try:
            self.recipe = Model.Recipe(pet, tutor, nutricionist, recipeName)
        except ValueError as err:
            raise(err)

        try:
            self.recipes_DB.addRecipe(self.recipe)
        except RuntimeError as err:
            raise(err)
        except ValueError as err:
            raise(err)
