
import pytest
from pytest import raises

# # from src.model.ingredient import Ingredient
# from src.model.ingredient_in_recipe import IngredientInRecipe
from src.data_base.ingredients_DB import IngredientsDB
# from src.data_base.recipes_DB import RecipesDB

from src.cozinha_pet.cozinha_pet import CozinhaPet


class TestCozinhaPet():

    #
    # Scenarios for Testing
    #

    # @pytest.fixture(scope="class")
    # def ingr_DB(self):
    #     DB = IngredientsDB()

    #     yield DB

    #     del(DB)

    # @ pytest.fixture(scope="class")
    # def reci_DB(self):
    #     DB = RecipesDB()

    #     yield DB

    #     del(DB)

    @ pytest.fixture(scope="class")
    def CP(self):
        _CP = CozinhaPet()

        yield _CP

        del(_CP)

    @pytest.fixture(scope="class")
    def ingredientData(self, DB):
        DB = IngredientsDB()

        try:
            ingredientDict = DB.Ingredients.find_one()

            newestActualFactor = DB.getNewestActualFactor(
                ingredientDict['_id']
            )
        except ValueError:
            raise RuntimeError('DB Vazio')

        yield (ingredientDict, newestActualFactor)

        del(newestActualFactor)
        del(ingredientDict)

    @pytest.fixture(scope="class")
    def ingredientAndRecipe_idData(self, ingr_DB, reci_DB):

        try:
            ingredientDict = ingr_DB.Ingredients.find_one()
            recipeDict = reci_DB.Recipes.find_one(
                {'petName': {'$exists': True}})
        except ValueError:
            raise RuntimeError('DB Vazio')

        yield (ingredientDict['_id'], recipeDict['_id'])

        del(ingredientDict)
        del(recipeDict)

    #
    # Assert Itens
    #

    # def assert_item_by_item(self, actual, expected, message=''):

    #     assert actual['name'] == expected['name'], message
    #     assert actual['searchable'] == expected['searchable'], message
    #     assert actual['type'] == expected['type'], message
    #     assert actual['unity'] == expected['unity'], message

    #     assert actual['establishedCostPer1K'] == \
    #         approx(expected['establishedCostPer1K'])

    #
    # Tests
    #

    #
    # Test Ingredients
    #

    def test_addIngredient_ok(self, CP):
        try:
            _id_1 = CP.addIngredient(
                '__teste_CP_01__', 'Vegetal', 'g', '3.45', '3.45')
        except ValueError as err:
            assert False, str(err)
        except RuntimeError as err:
            assert False, str(err)
        else:
            _id_2 = CP.ingredients_DB.getIngredient_id('__teste_CP_01__')
        finally:
            CP.remIngredient(_id_1)

        assert _id_1 == _id_2

    def test_addIngredient_bad_ingredient(self, CP):
        with raises(ValueError) as exception_info:
            CP.addIngredient('', 'Vegetal', 'g', '3.45', '3.45')

        assert exception_info.match('Nome do ingrediente inválido.')

    def test_addIngredient_ingredient_already_inserted(self, CP):
        try:
            _id_1 = CP.addIngredient(
                '__teste_CP_02__', 'Vegetal', 'g', '3.45', '3.45')
        except ValueError as err:
            assert False, str(err)
        except RuntimeError as err:
            assert False, str(err)

        with raises(ValueError) as exception_info:
            CP.addIngredient(
                '__teste_CP_02__', 'Vegetal', 'g', '3.45', '3.45')

        assert exception_info.match('Ingrediente já cadastrado.')

        CP.remIngredient(_id_1)

    def test_remIngredient_OK(self, CP):
        try:
            _id_1 = CP.addIngredient(
                '__teste_CP_03__', 'Vegetal', 'g', '3.45', '3.45')
        except ValueError as err:
            assert False, str(err)
        except RuntimeError as err:
            assert False, str(err)

        try:
            CP.remIngredient(_id_1)
        except ValueError as err:
            assert False, str(err)

        result = CP.ingredients_DB.Ingredients.find_one({'_id': _id_1})

        assert result is None

    def test_remIngredient_bad_ingredient(self, CP):
        wrong_id = -2
        with raises(ValueError) as exception_info:
            CP.remIngredient(wrong_id)

        assert exception_info.match(
            'Não foi possível deletar o ingrediente para remover.')

    #
    # Recipes
    #

    def test_addRecipe_ok(self, CP):
        try:
            _id_1, registrationNumber = CP.addRecipe(
                '__pet_CP_01__',
                '__tutor__',
                '__nutricionist__',
                '__recipe_name__')
        except ValueError as err:
            assert False, str(err)
        except RuntimeError as err:
            assert False, str(err)
        else:
            _id_2 = CP.recipes_DB.getRecipe_id(registrationNumber)
        finally:
            CP.remRecipe(_id_1)

        assert _id_1 == _id_2

    #
    # Ingredients And Recipes
    #

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_addIngredientToRecipe_OK(self, CP, ingredientAndRecipe_idData):

        ingredient_id, recipe_id = ingredientAndRecipe_idData

        try:
            CP.addIngredientToRecipe(recipe_id, ingredient_id, 0.35)
        except ValueError as err:
            assert False, str(err)

        try:
            CP.remIngredientFromRecipe(recipe_id, ingredient_id)
        except ValueError as err:
            assert False, str(err)

        # self.assert_item_by_item(ingredientInRecipe.dict, ingredient)

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_updateIngredientsInRecipeFromDB(self):
        assert False
