
import pytest
from pytest import approx, raises

# from src.model.ingredient import Ingredient
from src.model.ingredient_in_recipe import IngredientInRecipe
from src.data_base.ingredients_DB import IngredientsDB


class TestIngredientInRecipe():

    #
    # Scenarios for Testing
    #

    @pytest.fixture(scope="class")
    def DB(self):
        CP = IngredientsDB()

        yield CP

        del(CP)

    @pytest.fixture(scope="class")
    def ingredientData(self, DB):

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

    #
    # Assert Itens
    #

    def assert_item_by_item(self, actual, expected, message=''):

        assert actual['name'] == expected['name'], message
        assert actual['searchable'] == expected['searchable'], message
        assert actual['type'] == expected['type'], message
        assert actual['unity'] == expected['unity'], message

        assert actual['establishedCostPer1K'] == \
            approx(expected['establishedCostPer1K'])

    #
    # Test
    #

    def test_create_ingredient_OK(self, ingredientData):

        ingredient, newestActualFactor = ingredientData

        try:
            ingredientInRecipe = IngredientInRecipe(
                    ingredient,
                    newestActualFactor,
                    0.35)
        except ValueError:
            assert False

        self.assert_item_by_item(ingredientInRecipe.dict, ingredient)

    def test_create_ingredient_Bad_Dict_NoFields(self, ingredientData):

        ingredient, newestActualFactor = ingredientData

        ingredient_copy = ingredient.copy()

        del ingredient_copy['name']

        with raises(ValueError) as exception_info:
            IngredientInRecipe(
                ingredient_copy,
                newestActualFactor,
                0.35)

        assert exception_info.match(
            'O dicionário não possui todos os campos necessários')

    def test_create_ingredient_Bad_Dict_EmptyFields(self, ingredientData):

        ingredient, newestActualFactor = ingredientData

        ingredient_copy = ingredient.copy()

        ingredient_copy['name'] = ''

        with raises(ValueError) as exception_info:
            IngredientInRecipe(
                ingredient_copy,
                newestActualFactor,
                0.35)

        assert exception_info.match(
            'O dicionário não possui todos os valores necessários')

    def test_create_ingredient_Bad_Factor(self, ingredientData):

        ingredient, newestActualFactor = ingredientData

        with raises(ValueError) as exception_info:
            IngredientInRecipe(
                ingredient,
                'newestActualFactor',
                0.35)

        assert exception_info.match(
            'Fator atual do ingrediente inválido: '
            + str('newestActualFactor'))

    def test_create_ingredient_Bad_DailyAmount(self, ingredientData):

        ingredient, newestActualFactor = ingredientData

        with raises(ValueError) as exception_info:
            IngredientInRecipe(
                ingredient,
                newestActualFactor,
                '0,35')

        assert exception_info.match(
            'Quantidade diária do ingrediente inválida: ' + str('0,35'))
