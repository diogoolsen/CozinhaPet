
import datetime

import pytest
from pytest import approx, raises

from src.data_base.ingredients_DB import IngredientsDB
from src.model.ingredient import Ingredient
from src.model.cost_item import CostItem
from src.model.factors_item import FactorsItem


class TestIngredientsDB():

    #
    # Scenarios for Testing
    #

    @pytest.fixture(scope="class")
    def ing_DB(self):
        CP = IngredientsDB()

        yield CP

        del(CP)

    @pytest.fixture(scope="class")
    def ingredient_id(self, ing_DB):

        try:
            ing_DB.getIngredient_id('__teste_v1__')
        except ValueError:
            ingredient = Ingredient(
                '__teste_v1__', 'Vegetal', 'g', '3.45', '3.45')

            ing_DB.addIngredient(ingredient)

        _id = ing_DB.getIngredient_id('__teste_v1__')

        yield _id

        ing_DB.removeIngredient(_id)

    #
    # Testing Ingredients
    #

    def test_addIngredient(self, ing_DB, ingredient_id):

        actual = ing_DB.Ingredientes.find_one({'name': '__teste_v1__'})

        assert ingredient_id is not None
        assert actual['_id'] == ingredient_id

        assert actual['name'] == '__teste_v1__'
        assert actual['searchable'] == '__TESTE_V1__'
        assert actual['type'] == 'Vegetal'
        assert actual['unity'] == 'g'
        assert actual['establishedCostPer1K'] == approx(3.45)

        assert isinstance(actual['factorsLog'][0]['date'],
                          datetime.datetime)
        assert actual['factorsLog'][0]['cookingFactor'] == 1
        assert actual['factorsLog'][0]['safetyMargin'] == 1
        assert actual['factorsLog'][0]['actualFactor'] == 1

        assert isinstance(actual['costLog'][0]['date'],
                          datetime.datetime)
        assert actual['costLog'][0]['price'] == 3.45
        assert actual['costLog'][0]['amount'] == 1000.
        assert actual['costLog'][0]['costPer1Unity'] == approx(0.00345)
        assert actual['costLog'][0]['costPer1K'] == 3.45

    def test_addIngredient_duplicated(self, ing_DB, ingredient_id):

        ingredient = Ingredient('__teste_v1__', 'Vegetal', 'g', '3.45', '3.45')

        with raises(ValueError) as exception_info:
            # store the exception
            ing_DB.addIngredient(ingredient)

        # Check if ValueError contains correct message
        assert exception_info.match('Ingrediente já cadastrado.')

    def test_addIngredient_wrong_data(self, ing_DB, ingredient_id):

        ingredient = Ingredient('__teste_v1__', 'Vegetal', 'g', '3.45', '3.45')

        with raises(ValueError) as exception_info:
            # store the exception
            ing_DB.addIngredient(ingredient.dict)

        # Check if ValueError contains correct message
        assert exception_info.match('Tipo de dado do ingredite inválido.')

    def test_removeIngredient_wrong_id(self, ing_DB, ingredient_id):

        with raises(ValueError) as exception_info:
            # store the exception
            ing_DB.removeIngredient(12112)

        # Check if ValueError contains correct message
        assert exception_info.match('Não foi possível deletar o documento.')

    def test_removeIngredient(self, ing_DB, ingredient_id):

        ingredient = Ingredient('__teste_v2__', 'Vegetal', 'g', '3.45', '3.45')

        try:
            ing_DB.addIngredient(ingredient)
        except ValueError:
            assert False

        _id_v1 = ing_DB.Ingredientes.find_one({'name': '__teste_v2__'})['_id']

        try:
            ing_DB.removeIngredient(_id_v1)
        except ValueError:
            assert False

        _id_v2 = ing_DB.Ingredientes.find_one({'name': '__teste_v2__'})

        assert _id_v1 is not None
        assert _id_v2 is None

    def test_getIngredientsCursorByNameSimilarity(self, ing_DB):
        cursor = ing_DB.getIngredientsCursorByNameSimilarity('este_v')

        for item in cursor:
            assert item['name'] == '__teste_v1__'

    def test_getIngredientsNamesListBySimilarity(self, ing_DB):
        names_list = ing_DB.getIngredientsNamesListBySimilarity('este_v')

        assert names_list == ['__teste_v1__']

    def test_getIngredient_id_not_found(self, ing_DB):
        with raises(ValueError) as exception_info:
            # store the exception
            ing_DB.getIngredient_id('12112')

        # Check if ValueError contains correct message
        assert exception_info.match('Impossível encontrar ingrediente: 12112')

    def test_getIngredient_id(self, ing_DB):
        try:
            _id_v1 = ing_DB.getIngredient_id('__teste_v1__')
        except ValueError:
            assert False

        _id_v2 = ing_DB.Ingredientes.find_one(
            {'name': '__teste_v1__'}).get('_id')

        assert _id_v1 == _id_v2

    #
    # Testing Costs
    #

    def test_addNewCost(self, ing_DB, ingredient_id):
        costItem = CostItem(50, 500)

        try:
            ing_DB.addNewCost(ingredient_id, costItem)
        except RuntimeError as err:
            print(err)
            assert False
        except ValueError as err:
            print(err)
            assert False

        try:
            newestCost = ing_DB.getNewestCost(ingredient_id)
        except ValueError as err:
            print(err)
            assert False

        assert newestCost['price'] == approx(50)
        assert newestCost['amount'] == approx(500)
        assert newestCost['costPer1K'] == approx(100)
        assert newestCost['costPer1Unity'] == approx(0.1)

    def test_addNewCost_wrong_id(self, ing_DB, ingredient_id):
        costItem = CostItem(40, 400)

        with raises(RuntimeError) as exception_info:
            # store the exception
            ing_DB.addNewCost(122112, costItem)

        # Check if RuntimeError contains correct message
        assert exception_info.match('Custo não atualizado')

    def test_addNewCost_wrong_data(self, ing_DB, ingredient_id):
        with raises(ValueError) as exception_info:
            # store the exception
            ing_DB.addNewCost(ingredient_id, (50, 500))

        # Check if ValueError contains correct message
        assert exception_info.match('Tipo de dado do custo inválido.')

    def test_getNewCost(self, ing_DB, ingredient_id):
        costItem = CostItem(55, 550)

        try:
            ing_DB.addNewCost(ingredient_id, costItem)
        except RuntimeError as err:
            print(err)
            assert False
        except ValueError as err:
            print(err)
            assert False

        try:
            newestCost = ing_DB.getNewestCost(ingredient_id)
            newestCost1K = ing_DB.getNewestCost1K(ingredient_id)
            newestCost1Unity = ing_DB.getNewestCost1Unity(ingredient_id)
        except ValueError as err:
            print(err)
            assert False

        assert newestCost1K == approx(100)
        assert newestCost1Unity == approx(0.1)
        assert newestCost['price'] == approx(55)
        assert newestCost['amount'] == approx(550)
        assert newestCost['costPer1K'] == approx(100)
        assert newestCost['costPer1Unity'] == approx(0.1)
        assert isinstance(newestCost['date'], datetime.datetime)

    def test_getNewCost_wrong_id(self, ing_DB):
        with raises(ValueError) as exception_info:
            # store the exception
            ing_DB.getNewestCost(12342134)

        # Check if ValueError contains correct message
        assert exception_info.match('Pesquisa de custo mais recente falhou.')

        with raises(ValueError) as exception_info:
            # store the exception
            ing_DB.getNewestCost1K(12341321432)

        # Check if ValueError contains correct message
        assert exception_info.match('Pesquisa de custo mais recente falhou.')

        with raises(ValueError) as exception_info:
            # store the exception
            ing_DB.getNewestCost1Unity(141233421321243)

        # Check if ValueError contains correct message
        assert exception_info.match('Pesquisa de custo mais recente falhou.')

    #
    # Testing Factors
    #

    def test_addNewFactors(self, ing_DB, ingredient_id):
        factorsItem = FactorsItem(0.5, 2)

        try:
            ing_DB.addNewFactors(ingredient_id, factorsItem)
        except RuntimeError as err:
            print(err)
            assert False
        except ValueError as err:
            print(err)
            assert False

        try:
            newestFactors = ing_DB.getNewestFactors(ingredient_id)
        except ValueError as err:
            print(err)
            assert False

        assert newestFactors['cookingFactor'] == approx(0.5)
        assert newestFactors['safetyMargin'] == approx(2)
        assert newestFactors['actualFactor'] == approx(1)

    def test_addNewFactors_wrong_id(self, ing_DB, ingredient_id):
        factorsItem = FactorsItem(0.5, 2)

        with raises(RuntimeError) as exception_info:
            # store the exception
            ing_DB.addNewFactors(122112, factorsItem)

        # Check if RuntimeError contains correct message
        assert exception_info.match('Fatores não atualizados')

    def test_addNewFactors_wrong_data(self, ing_DB, ingredient_id):
        with raises(ValueError) as exception_info:
            # store the exception
            ing_DB.addNewFactors(ingredient_id, (50, 500))

        # Check if ValueError contains correct message
        assert exception_info.match('Tipo de dado dos fatores é inválido.')

    def test_getNewFactors(self, ing_DB, ingredient_id):
        factorsItem = FactorsItem(0.75, 1.1)

        try:
            ing_DB.addNewFactors(ingredient_id, factorsItem)
        except RuntimeError as err:
            print(err)
            assert False
        except ValueError as err:
            print(err)
            assert False

        try:
            newestFactors = ing_DB.getNewestFactors(ingredient_id)
            newestFactorsCooking = ing_DB.getNewestCookingFactor(ingredient_id)
            newestFactorsSafety = ing_DB.getNewestSafetyMargin(ingredient_id)
            newestFactorsActual = ing_DB.getNewestActualFactor(ingredient_id)
        except ValueError as err:
            print(err)
            assert False

        assert newestFactorsCooking == approx(0.75)
        assert newestFactorsSafety == approx(1.1)
        assert newestFactorsActual == approx(0.825)
        assert newestFactors['cookingFactor'] == approx(0.75)
        assert newestFactors['safetyMargin'] == approx(1.1)
        assert newestFactors['actualFactor'] == approx(0.825)
        assert isinstance(newestFactors['date'], datetime.datetime)

    def test_getNewFactors_wrong_id(self, ing_DB):
        with raises(ValueError) as exception_info:
            # store the exception
            ing_DB.getNewestFactors(12342134)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'Pesquisa de Fatores mais recentes falhou.')

        with raises(ValueError) as exception_info:
            # store the exception
            ing_DB.getNewestCookingFactor(12341321432)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'Pesquisa de Fatores mais recentes falhou.')

        with raises(ValueError) as exception_info:
            # store the exception
            ing_DB.getNewestSafetyMargin(141233421321243)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'Pesquisa de Fatores mais recentes falhou.')

        with raises(ValueError) as exception_info:
            # store the exception
            ing_DB.getNewestActualFactor(141233421321243)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'Pesquisa de Fatores mais recentes falhou.')
