
# import datetime

import pytest
from pytest import raises  # approx

from pymongo.collection import ReturnDocument

from src.data_base.recipes_DB import RecipesDB
from src.model.recipe import Recipe


class TestRecipesDB():

    #
    # Scenarios for Testing
    #

    @pytest.fixture(scope="class")
    def recipes_DB(self):
        RDB = RecipesDB()

        yield RDB

        del(RDB)

    @pytest.fixture(scope="class")
    def recipe_id(self, recipes_DB):

        recipe = Recipe('__pet__1',
                        '__tutor__',
                        '__nutricionist__',
                        '__recipe_name__')

        registrationNumber = recipes_DB.addRecipe(recipe)

        _id = recipes_DB.getRecipe_id(registrationNumber)

        yield ({'_id': _id, 'registrationNumber': registrationNumber})

        recipes_DB.removeRecipe(_id)

    def test_getAndIncrementRecipesCount(self, recipes_DB):
        previous = recipes_DB.Recipes.find_one(
            {'recipesAccumulator': {'$exists': True}}
            ).get('recipesAccumulator')

        new = recipes_DB.getAndIncrementRecipesAccumulator()

        check = recipes_DB.Recipes.find_one(
            {'recipesAccumulator': {'$exists': True}}
            ).get('recipesAccumulator')

        assert previous + 1 == new
        assert new == check

    def test_addRecipe_OK(self, recipes_DB):
        recipe_1 = Recipe('__pet__2',
                          '__tutor__',
                          '__nutricionist__',
                          '__recipe_name__')

        registrationNumber_1 = recipes_DB.addRecipe(recipe_1)

        _id_1 = recipes_DB.getRecipe_id(registrationNumber_1)

        recipe_2 = Recipe('__pet__3',
                          '__tutor__',
                          '__nutricionist__',
                          '__recipe_name__')

        registrationNumber_2 = recipes_DB.addRecipe(recipe_2)

        _id_2 = recipes_DB.getRecipe_id(registrationNumber_2)

        recipes_DB.removeRecipe(_id_1)
        recipes_DB.removeRecipe(_id_2)

        assert registrationNumber_1 == registrationNumber_2 - 1
        assert _id_1 != _id_2

    def test_addRecipe_Bad_Recipe(self, recipes_DB):
        with raises(ValueError) as exception_info:
            # store the exception
            recipes_DB.addRecipe('ingredient')

        # Check if ValueError contains correct message
        assert exception_info.match('Tipo de dado da receita inválido.')

    def test_addRecipe_compromised_registrationNumber(self, recipes_DB):
        recipe_1 = Recipe('__pet__4',
                          '__tutor__',
                          '__nutricionist__',
                          '__recipe_name__')

        recipe_2 = Recipe('__pet__5',
                          '__tutor__',
                          '__nutricionist__',
                          '__recipe_name__')

        registrationNumber_1 = recipes_DB.addRecipe(recipe_1)

        _id_1 = recipes_DB.getRecipe_id(registrationNumber_1)

        decremented = recipes_DB.Recipes.find_one_and_update(
            filter={'recipesAccumulator': {'$exists': True}},
            update={'$inc': {'recipesAccumulator': -1}},
            return_document=ReturnDocument.AFTER
        )['recipesAccumulator']

        assert decremented + 1 == registrationNumber_1

        with raises(RuntimeError) as exception_info:
            # store the exception
            recipes_DB.addRecipe(recipe_2)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'Integridade do registrationNumber comprometida.')

        # _id_2 = recipes_DB.getRecipe_id(registrationNumber_2)

        recipes_DB.removeRecipe(_id_1)

        check = recipes_DB.Recipes.find_one(
            {'recipesAccumulator': {'$exists': True}}
            ).get('recipesAccumulator')

        incremented = recipes_DB.Recipes.find_one_and_update(
            filter={'recipesAccumulator': {'$exists': True}},
            update={'$inc': {'recipesAccumulator': 1}},
            return_document=ReturnDocument.AFTER
        )['recipesAccumulator']

        assert check + 1 == incremented

    def test_getRecipe_id(self):
        print('Continuar testando da função getRecipe_id para baixo')
        assert False
