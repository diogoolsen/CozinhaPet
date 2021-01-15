
# import re

# import unidecode

# from pymongo import MongoClient
# from pymongo.errors import ConnectionFailure

from src.model.recipe import Recipe
from data_base.cozinha_pet_database import CozinhaPetDataBase


class RecipesDB(CozinhaPetDataBase):

    # def __init__(self):

    #     try:
    #         # Client connects to "localhost" by default
    #         self.client = MongoClient()
    #     except ConnectionFailure:
    #         raise RuntimeError('Banco de Dados indisponível.')

    #     # Create local 'CozinhaPetDB' database on the fly
    #     # Acessa o banco de dados 'CozinhaPetDB'
    #     self.CozinhaPetDB = self.client.CozinhaPetDB

    #     # Acessa a coleção 'Ingredientes'
    #     self.Recipes = self.CozinhaPetDB.Recipes

    # def __del__(self):
    #     self.client.close

    # def getSearchableRegex(self, term):
    #     # Remove caracteres estranhos
    #     searchable = unidecode.unidecode(term).upper()
    #     # Gera a expressão regular
    #     regx = re.compile(r'(?i)^{}$'.format(searchable))

    #     return regx

    #
    # Manipulate Recipes
    #

    def addRecipe(self, recipe):
        # Verificar se já não está no banco

        if not isinstance(recipe, Recipe):
            raise ValueError('Tipo de dado da receita inválido.')
        else:
            dict = recipe.dict

        self.Recipes.insert_one(dict)

    def getRecipeCursorByTermSimilarity(self, term):

        regx = self.getSearchableRegex(term)

        recipesList = self.Ingredientes.find(
                    {'searchable': regx},
                    {'_id': 0, 'name': 1}
                ).distinct('name')
        
        return recipesList

        # ingredient = self.Ingredientes.find_one({'name': regx}, {'_id': 1})

        # if ingredient is None:
        #     raise ValueError('Impossível encontrar ingrediente: ' + name)

        # return ingredient.get('_id')

    def removeRecipe(self, _id):
        result = self.Ingredientes.delete_one({'_id': _id})
        if result.deleted_count == 0:
            raise ValueError('Não foi possível deletar o documento.')

    # def getAllIngredientsCursor(self):
    #     return self.Ingredientes.find()

    # def getIngredientsCursorByNameSimilarity(self, name):
    #     regx = re.compile(r'(?i){}'.format(name))

    #     return self.Ingredientes.find(
    #             {'searchable': regx}
    #         )

    # def getIngredientsNamesListBySimilarity(self, name):
    #     regx = re.compile(r'(?i){}'.format(name))

    #     ingredientNamesList = self.Ingredientes.find(
    #         {'searchable': regx},
    #         {'_id': 0, 'name': 1}
    #     ).distinct('name')

    #     return ingredientNamesList

    # def getIngredient_id(self, name):
    #     regx = re.compile(r'(?i)^{}$'.format(name))

    #     ingredient = self.Ingredientes.find_one({'name': regx}, {'_id': 1})

    #     if ingredient is None:
    #         raise ValueError('Impossível encontrar ingrediente: ' + name)

    #     return ingredient.get('_id')

    # #
    # # Manipulate Costs
    # #

    # def addNewCost(self, _id, costItem):
    #     if not isinstance(costItem, CostItem):
    #         raise ValueError('Tipo de dado do custo inválido.')

    #     result = self.Ingredientes.update_one(
    #             {'_id': _id},
    #             {'$push': {'costLog': costItem.dict}}
    #         )

    #     if result.modified_count != 1:
    #         raise RuntimeError('Custo não atualizado')

    # def getNewestCost(self, _id):
    #     cursor = self.Ingredientes.aggregate([
    #             {'$match': {'_id': _id}},
    #             {'$project': {
    #                 'costLog': 1,
    #                 '_id': 0}},
    #             {'$unwind': {'path': '$costLog'}},
    #             {'$sort': {'costLog.date': -1}},
    #             {'$limit': 1}
    #         ])

    #     newestCost = list(cursor)

    #     if len(newestCost) != 1:
    #         raise ValueError('Pesquisa de custo mais recente falhou.')

    #     return newestCost[0]['costLog']

    # def getNewestCost1Unity(self, _id):
    #     try:
    #         ingredientNewestCostItem = self.getNewestCost(_id)
    #     except ValueError as err:
    #         raise err

    #     return ingredientNewestCostItem['costPer1Unity']

    # def getNewestCost1K(self, _id):
    #     try:
    #         ingredientNewestCostItem = self.getNewestCost(_id)
    #     except ValueError as err:
    #         raise err

    #     return ingredientNewestCostItem['costPer1K']

    # #
    # # Manipulate Factors
    # #

    # def addNewFactors(self, _id, newFactorsItem):
    #     if not isinstance(newFactorsItem, FactorsItem):
    #         raise ValueError('Tipo de dado dos fatores é inválido.')

    #     result = self.Ingredientes.update_one(
    #         {'_id': _id},
    #         {'$push': {'factorsLog': newFactorsItem.dict}}
    #     )

    #     if result.modified_count != 1:
    #         raise RuntimeError('Fatores não atualizados')

    # def getNewestFactors(self, _id):
    #     cursor = self.Ingredientes.aggregate([
    #         {'$match': {'_id': _id}},
    #         {'$project': {
    #             'factorsLog': 1,
    #             '_id': 0}},
    #         {'$unwind': {'path': '$factorsLog'}},
    #         {'$sort': {'factorsLog.date': -1}},
    #         {'$limit': 1}
    #     ])

    #     newestFactors = list(cursor)

    #     if len(newestFactors) != 1:
    #         raise ValueError('Pesquisa de Fatores mais recentes falhou.')

    #     return newestFactors[0]['factorsLog']

    # def getNewestCookingFactor(self, _id):
    #     try:
    #         ingredientNewestFactorsItem = self.getNewestFactors(_id)
    #     except ValueError as err:
    #         raise err

    #     return ingredientNewestFactorsItem['cookingFactor']

    # def getNewestSafetyMargin(self, _id):
    #     try:
    #         ingredientNewestFactorsItem = self.getNewestFactors(_id)
    #     except ValueError as err:
    #         raise err

    #     return ingredientNewestFactorsItem['safetyMargin']

    # def getNewestActualFactor(self, _id):
    #     try:
    #         ingredientNewestFactorsItem = self.getNewestFactors(_id)
    #     except ValueError as err:
    #         raise err

    #     return ingredientNewestFactorsItem['actualFactor']
