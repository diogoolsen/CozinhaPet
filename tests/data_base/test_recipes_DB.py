
import datetime

import pytest
from pytest import raises  # approx

from pymongo.collection import ReturnDocument

from src.data_base.recipes_DB import RecipesDB
from src.data_base.ingredients_DB import IngredientsDB
from src.model import Recipe, IngredientInRecipe


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

        recipe = Recipe('__pet__1__',
                        '__tutor__',
                        '__nutricionist__',
                        '__recipe_name__')

        _id, registrationNumber = recipes_DB.addRecipe(recipe)

        _id = recipes_DB.getRecipe_id(registrationNumber)

        yield (_id, registrationNumber)

        recipes_DB.removeRecipe(_id)

    @pytest.fixture(scope="class")
    def recipe_with_ingredients(self, recipes_DB):

        recipe = Recipe('__pet__2__',
                        '__tutor__',
                        '__nutricionist__',
                        '__recipe_name__')

        recipe_id, registrationNumber = recipes_DB.addRecipe(recipe)

        quantidade = 3

        ingr_DB = IngredientsDB()

        #
        # Pegar IDs de Ingredientes
        #

        ingredients_idsList = list(
            ingr_DB.Ingredients.find({}, {'_id': 1}).limit(quantidade))

        for ingredient_id in ingredients_idsList:

            #
            # Gera os objetos IngredientInRecipe
            #

            ingredient = ingr_DB.getIngredientBy_id(ingredient_id['_id'])
            newestFactors = ingr_DB.getNewestActualFactor(
                ingredient_id['_id'])

            ingredientInRecipe = IngredientInRecipe(
                ingredient, newestFactors, 0.35)

            #
            # Insere os ingredientes na receita de teste
            #

            recipes_DB.addIngredientToRecipe(recipe_id, ingredientInRecipe)

        if len(recipes_DB.getIngredientsListFromRecipe(recipe_id))\
                != quantidade:
            assert False

        yield (ingredients_idsList, recipe_id)

        recipes_DB.removeRecipe(recipe_id)

    @pytest.fixture(scope="class")
    def ingredientInRecipe(self):
        # Pegar IDs de um Ingrediente
        ingr_DB = IngredientsDB()

        ingredient_id = ingr_DB.Ingredients.find_one({}, {'_id': 1})

        # Gera os objetos IngredientInRecipe
        ingredient = ingr_DB.getIngredientBy_id(ingredient_id['_id'])
        newestFactors = ingr_DB.getNewestActualFactor(
            ingredient_id['_id'])

        ingredientInRecipe = IngredientInRecipe(
            ingredient, newestFactors, 0.35)

        yield ingredientInRecipe

        del(ingredientInRecipe)

    #
    # test Recipes Number
    #

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

    #
    # isRecipeInDB
    #

    def test_isRecipeInDB_OK(self, recipes_DB, recipe_with_ingredients):

        ingredients_idsList, recipe_id = recipe_with_ingredients

        result = recipes_DB.isRecipeInDB(recipe_id)

        if not result:
            assert False

    def test_isRecipeInDB_bad_recipe_id(self, recipes_DB):

        wrong_id = -2
        with raises(ValueError) as exception_info:
            recipes_DB.isRecipeInDB(wrong_id)

        assert exception_info.match(
            'Impossível encontrar receita _id: ' + str(wrong_id))

    #
    # addRecipe
    #

    def test_addRecipe_OK(self, recipes_DB):
        recipe_1 = Recipe('__pet__2',
                          '__tutor__',
                          '__nutricionist__',
                          '__recipe_name__')

        _id_1, registrationNumber_1 = recipes_DB.addRecipe(recipe_1)

        print(_id_1)
        print(registrationNumber_1)

        recipe_2 = Recipe('__pet__3',
                          '__tutor__',
                          '__nutricionist__',
                          '__recipe_name__')

        _id_2, registrationNumber_2 = recipes_DB.addRecipe(recipe_2)

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

        _id_1, registrationNumber_1 = recipes_DB.addRecipe(recipe_1)

        # _id_1 = recipes_DB.getRecipe_id(registrationNumber_1)

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

    #
    # getRecipe_id
    #

    def test_getRecipe_id_Bad_RegistrationNumber(self, recipes_DB):

        wrong_id = -1

        with raises(ValueError) as exception_info:
            # store the exception
            recipes_DB.getRecipe_id(wrong_id)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'Impossível encontrar receita: ' + str(wrong_id))

    def test_getRecipe_id_RegistrationNumber_compromised(self, recipes_DB):

        recipe_1 = Recipe('__pet__6',
                          '__tutor__',
                          '__nutricionist__',
                          '__recipe_name__')

        recipe_2 = Recipe('__pet__7',
                          '__tutor__',
                          '__nutricionist__',
                          '__recipe_name__')

        _id_1, registrationNumber_1 = recipes_DB.addRecipe(recipe_1)
        _id_2, registrationNumber_2 = recipes_DB.addRecipe(recipe_2)

        registrationNumberDecremented = recipes_DB.Recipes.find_one_and_update(
            filter={'_id': _id_2},
            update={'$set': {'registrationNumber': registrationNumber_1}},
            return_document=ReturnDocument.AFTER
        )['registrationNumber']

        with raises(RuntimeError) as exception_info:
            # store the exception
            recipes_DB.getRecipe_id(registrationNumberDecremented)

        assert exception_info.match(
            'Integridade do registrationNumber comprometida - '
            'registrationNumber: ' + str(registrationNumberDecremented))

        recipes_DB.removeRecipe(_id_1)
        recipes_DB.removeRecipe(_id_2)

    def test_getRecipe_id_OK(self, recipes_DB):

        recipe = Recipe('__pet__8',
                        '__tutor__',
                        '__nutricionist__',
                        '__recipe_name__')

        _id_1, registrationNumber = recipes_DB.addRecipe(recipe)

        _id_2 = recipes_DB.getRecipe_id(registrationNumber)

        assert _id_1 == _id_2

        recipes_DB.removeRecipe(_id_1)

    def assertRecipes_Metadata(self, actual, expected):

        assert actual['petName'] == expected['petName']
        assert actual['petSearchable'] == expected['petSearchable']
        assert actual['tutorName'] == expected['tutorName']
        assert actual['tutorSearchable'] == expected['tutorSearchable']
        assert actual['nutricionistName'] == expected['nutricionistName']
        assert actual['nutricionistSeachable'] ==\
            expected['nutricionistSeachable']
        assert actual['recipeName'] == expected['recipeName']
        assert actual['recipeNameSearchable'] ==\
            expected['recipeNameSearchable']
        assert actual['registrationNumber'] == expected['registrationNumber']
        assert isinstance(actual['date'], datetime.datetime)

    def test_getRecipeByRegistrationNumber(self, recipes_DB):
        recipe = Recipe('__pet__9',
                        '__tutor__',
                        '__nutricionist__',
                        '__recipe_name__')

        _id, registrationNumber = recipes_DB.addRecipe(recipe)

        returnedRecipe = recipes_DB.getRecipeByRegistrationNumber(
            registrationNumber)

        self.assertRecipes_Metadata(recipe.dict, returnedRecipe)

        recipes_DB.removeRecipe(_id)

    def test_getRecipeByRegistrationNumber_ok(self, recipes_DB):
        recipe = Recipe('__pet__10',
                        '__tutor__',
                        '__nutricionist__',
                        '__recipe_name__')

        _id, registrationNumber = recipes_DB.addRecipe(recipe)

        returnedRecipe = recipes_DB.getRecipeByRegistrationNumber(
            registrationNumber)

        self.assertRecipes_Metadata(recipe.dict, returnedRecipe)

        recipes_DB.removeRecipe(_id)

    def test_getRecipeByRegistrationNumber_Bad_reristrationNumber(self,
                                                                  recipes_DB):

        badRegistrationNumber = -2

        with raises(ValueError) as exception_info:
            recipes_DB.getRecipeByRegistrationNumber(badRegistrationNumber)

        assert exception_info.match('Impossível encontrar receita: '
                                    + str(badRegistrationNumber))

    def test_getRecipeBy_id_ok(self, recipes_DB):
        recipe = Recipe('__pet__10',
                        '__tutor__',
                        '__nutricionist__',
                        '__recipe_name__')

        _id, registrationNumber = recipes_DB.addRecipe(recipe)

        returnedRecipe = recipes_DB.getRecipeBy_id(_id)

        self.assertRecipes_Metadata(recipe.dict, returnedRecipe)

        recipes_DB.removeRecipe(_id)

    def test_getRecipeBy_id_Bad_id(self, recipes_DB):
        bad_id = -2

        with raises(ValueError) as exception_info:
            recipes_DB.getRecipeBy_id(bad_id)

        assert exception_info.match('Impossível encontrar receita _id: '
                                    + str(bad_id))

    def test_getRecipeCursorByTermSimilarity_OK(self, recipes_DB):
        recipe_1 = Recipe('__pet__XYZ_',
                          '__tutor__IJK_',
                          '__nutricionist__',
                          '__recipe_name__')

        recipe_2 = Recipe('__pet__10',
                          '__tutor__',
                          '__nutricionist__',
                          '__recipe_name__IJK_')

        _id_1, registrationNumber_1 = recipes_DB.addRecipe(recipe_1)
        _id_2, registrationNumber_2 = recipes_DB.addRecipe(recipe_2)

        cursor = recipes_DB.getRecipeCursorByTermSimilarity('XYZ')

        assert len(list(cursor)) == 1

        cursor = recipes_DB.getRecipeCursorByTermSimilarity('xyz ijk')

        assert len(list(cursor)) == 2

        cursor = recipes_DB.getRecipeCursorByTermSimilarity('ijk')

        assert len(list(cursor)) == 2

        cursor = recipes_DB.getRecipeCursorByTermSimilarity('WERTR')

        assert len(list(cursor)) == 0

        recipes_DB.removeRecipe(_id_1)
        recipes_DB.removeRecipe(_id_2)

    def test_getRecipeCursorByTermSimilarity_bad_search(self, recipes_DB):
        cursor = recipes_DB.getRecipeCursorByTermSimilarity(
            'bhw234bk3 njkm234b hkjds3')

        assert len(list(cursor)) == 0

    def test_removeRecipe_OK(self, recipes_DB):
        recipe = Recipe('__pet__11',
                        '__tutor__',
                        '__nutricionist__',
                        '__recipe_name__')

        _id, registrationNumber = recipes_DB.addRecipe(recipe)

        recipes_DB.removeRecipe(_id)

        assert recipes_DB.Recipes.find_one({'_id': _id}) is None

    def test_removeRecipe_Bad_id(self, recipes_DB):
        bad_id = -2

        with raises(ValueError) as exception_info:
            recipes_DB.removeRecipe(bad_id)

        assert exception_info.match(
            'Não foi possível deletar o documento _id: ' + str(bad_id))

    # #
    # # findIngredientInRecipe
    # #

    # # @pytest.mark.skip(reason="no way of currently testing this")
    # def test_findIngredientInRecipe_OK(self,
    #                                    recipes_DB,
    #                                    recipe_with_ingredients):

    #     ingredients_idsList, recipe_id = recipe_with_ingredients

    #     ingredient = recipes_DB.findIngredientInRecipe(
    #         recipe_id,
    #         ingredients_idsList[0]['_id'])

    #     assert False, str(ingredient)

    # @pytest.mark.skip(reason="no way of currently testing this")
    # def test_findIngredientInRecipe_bad_recipe_id(self, recipes_DB):
    #     assert False

    # @pytest.mark.skip(reason="no way of currently testing this")
    # def test_findIngredientInRecipe_bad_ingredient_id(self, recipes_DB):
    #     assert False

    #
    # isIngredientInRecipe
    #

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_isIngredientInRecipe_OK_true(self,
                                          recipes_DB,
                                          recipe_with_ingredients):

        ingredients_idsList, recipe_id = recipe_with_ingredients

        if recipes_DB.isIngredientInRecipe(recipe_id,
                                           ingredients_idsList[0]['_id']):
            assert True
        else:
            assert False

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_isIngredientInRecipe_OK_false(self,
                                           recipes_DB,
                                           recipe_with_ingredients):

        ingredients_idsList, recipe_id = recipe_with_ingredients

        if not recipes_DB.isIngredientInRecipe(recipe_id, -2):
            assert True
        else:
            assert False

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_isIngredientInRecipe_bad_recipe_id(self,
                                                recipes_DB,
                                                recipe_with_ingredients):

        ingredients_idsList, recipe_id = recipe_with_ingredients

        if not recipes_DB.isIngredientInRecipe(-2,
                                               ingredients_idsList[0]['_id']):
            assert True
        else:
            assert False

    #
    # addIngredientToRecipe
    #

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_addIngredientToRecipe_OK(self, recipes_DB, ingredientInRecipe):

        recipe = Recipe('__pet__13',
                        '__tutor__',
                        '__nutricionist__',
                        '__recipe_name__')

        recipe_id, registrationNumber = recipes_DB.addRecipe(recipe)

        # Insere o ingrediente na receita de teste
        recipes_DB.addIngredientToRecipe(recipe_id, ingredientInRecipe)

        if len(recipes_DB.getIngredientsListFromRecipe(recipe_id)) != 1:
            assert False

        recipes_DB.removeRecipe(recipe_id)

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_addIngredientToRecipe_ingredisnte_alredy_in_recipe(
                self, recipes_DB, ingredientInRecipe):

        recipe = Recipe('__pet__14',
                        '__tutor__',
                        '__nutricionist__',
                        '__recipe_name__')

        recipe_id, registrationNumber = recipes_DB.addRecipe(recipe)

        # Insere o ingrediente na receita de teste
        recipes_DB.addIngredientToRecipe(recipe_id, ingredientInRecipe)

        if len(recipes_DB.getIngredientsListFromRecipe(recipe_id)) != 1:
            assert False

        with raises(ValueError) as exception_info:
            # REinsere o ingrediente na receita de teste
            recipes_DB.addIngredientToRecipe(recipe_id, ingredientInRecipe)

        assert exception_info.match(
            'Ingrediente já inserido na receita - '
            'Atualize seu valor.')

        recipes_DB.removeRecipe(recipe_id)

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_addIngredientToRecipe_bad_recipe_id(self,
                                                 recipes_DB,
                                                 ingredientInRecipe):
        wrong_id = -2

        with raises(ValueError) as exception_info:
            # REinsere o ingrediente na receita de teste
            recipes_DB.addIngredientToRecipe(wrong_id, ingredientInRecipe)

        assert exception_info.match(
            'Impossível encontrar receita _id: ' + str(wrong_id))

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_addIngredientToRecipe_bad_ingredient(self,
                                                  recipes_DB,
                                                  recipe_id):
        _id, registrationNumber = recipe_id
        with raises(ValueError) as exception_info:
            # REinsere o ingrediente na receita de teste
            recipes_DB.addIngredientToRecipe(_id, 'wrong_id')

        assert exception_info.match(
            'Tipo de dado do ingrediente da receita inválido.')

    #
    # remIngredientFromRecipe
    #

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_remIngredientFromRecipe_OK(self,
                                        recipes_DB,
                                        recipe_with_ingredients):

        ingredients_idsList, recipe_id = recipe_with_ingredients

        firstList = recipes_DB.getIngredientsListFromRecipe(recipe_id)

        recipes_DB.remIngredientFromRecipe(recipe_id,
                                           ingredients_idsList[0]['_id'])

        lastList = recipes_DB.getIngredientsListFromRecipe(recipe_id)

        if len(firstList) != len(lastList) + 1:
            assert False

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_remIngredientFromRecipe_bad_recipe_id(self,
                                                   recipes_DB,
                                                   ingredientInRecipe):
        wrong_id = -2

        with raises(ValueError) as exception_info:
            # REinsere o ingrediente na receita de teste
            recipes_DB.remIngredientFromRecipe(wrong_id, ingredientInRecipe)

        assert exception_info.match(
            'Impossível encontrar receita _id: ' + str(wrong_id))

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_remIngredientFromRecipe_bad_ingredient_id(self,
                                                       recipes_DB,
                                                       recipe_id):
        _id, registrationNumber = recipe_id

        with raises(ValueError) as exception_info:
            # REinsere o ingrediente na receita de teste
            recipes_DB.remIngredientFromRecipe(_id, 'wrong_id')

        assert exception_info.match('Ingrediente não inserido na receita.')

    #
    # getIngredientsListFromRecipe
    #

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_getIngredientsListFromRecipe_OK(self, recipes_DB):

        recipe = Recipe('__pet__12',
                        '__tutor__',
                        '__nutricionist__',
                        '__recipe_name__')

        recipe_id, registrationNumber = recipes_DB.addRecipe(recipe)

        quantidade = 3

        ingr_DB = IngredientsDB()

        #
        # Pegar IDs de Ingredientes
        #

        ingredients_idsList = list(
            ingr_DB.Ingredients.find({}, {'_id': 1}).limit(quantidade))

        for ingredient_id in ingredients_idsList:

            #
            # Gera os objetos IngredientInRecipe
            #

            ingredient = ingr_DB.getIngredientBy_id(ingredient_id['_id'])
            newestFactors = ingr_DB.getNewestActualFactor(
                ingredient_id['_id'])

            ingredientInRecipe = IngredientInRecipe(
                ingredient, newestFactors, 0.35)

            #
            # Insere os ingredientes na receita de teste
            #

            recipes_DB.addIngredientToRecipe(recipe_id, ingredientInRecipe)

        if len(recipes_DB.getIngredientsListFromRecipe(recipe_id))\
                != quantidade:
            assert False

        recipes_DB.removeRecipe(recipe_id)

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_getIngredientsListFromRecipe_Bad_id(self, recipes_DB):
        bad_id = -2

        with raises(ValueError) as exception_info:
            recipes_DB.getIngredientsListFromRecipe(bad_id)

        assert exception_info.match(
            'Impossível encontrar receita _id: ' + str(bad_id))

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_getIngredientsListFromRecipe_empty_list(self, recipes_DB):
        recipe = Recipe('__pet__13',
                        '__tutor__',
                        '__nutricionist__',
                        '__recipe_name__')

        recipe_id, registrationNumber = recipes_DB.addRecipe(recipe)

        if len(recipes_DB.getIngredientsListFromRecipe(recipe_id))\
                != 0:
            assert False

        recipes_DB.removeRecipe(recipe_id)
