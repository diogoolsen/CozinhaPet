
from pymongo.collection import ReturnDocument

from src.model.recipe import Recipe
from src.data_base.cozinha_pet_database import CozinhaPetDataBase


class RecipesDB(CozinhaPetDataBase):

    #
    # Manipulate Recipes Number
    #

    # Sei que esta não é a melhor abordagem, sei que o Pymongo
    # não implementa autoincrement, porém a marcela que um ID
    # autoincrementado para controle pessoal da receita
    # portanto resolvi implementar assim
    # Como o sistema não terá acessos concorrentes, deve funcionar

    def getAndIncrementRecipesAccumulator(self):

        accumulator = self.Recipes.find_one_and_update(
            filter={'recipesAccumulator': {'$exists': True}},
            update={'$inc': {'recipesAccumulator': 1}},
            # Cria o documento caso não exista
            upsert=True,
            # Retorna o documento após atualizar o valor
            # ou seja, retorna já o novo valor
            return_document=ReturnDocument.AFTER
        )

        return accumulator['recipesAccumulator']

    #
    # Manipulate Recipes
    #

    def addRecipe(self, recipe):
        # Verificar se já não está no banco

        if not isinstance(recipe, Recipe):
            raise ValueError('Tipo de dado da receita inválido.')
        else:
            dict = recipe.dict
            # Recebe e Incrementa o número da receita
            recipesAccumulator = self.getAndIncrementRecipesAccumulator()

            # Verifica se o registrationNumber já não existe,
            # Caso exista a integridade do valor foi comprometida
            # Lembrar que esta abordagem não é recomendada pelo MongoDB
            if self.Recipes.find_one(
                    {'registrationNumber': recipesAccumulator}
                    ) is not None:

                raise RuntimeError(
                    'Integridade do registrationNumber comprometida.')

            dict['registrationNumber'] = recipesAccumulator

        _id = self.Recipes.insert_one(dict)

        return (_id.inserted_id, recipesAccumulator)

    def getRecipe_id(self, registrationNumber):
        cursor = self.Recipes.find(
            {'registrationNumber': registrationNumber}, {'_id': 1})

        # Verifica se retornou algum resultado e se não há mais do que um
        # resultado
        # Caso tenha voltado mais que um resultado a integridade de
        # registrationNumber está comprometida
        id_list = list(cursor)
        if len(id_list) == 0:
            raise ValueError(
                'Impossível encontrar receita: ' + str(registrationNumber))
        elif len(id_list) > 1:
            raise RuntimeError(
                'Integridade do registrationNumber comprometida - '
                'registrationNumber: ' + str(registrationNumber))

        return id_list[0]['_id']

    def getRecipeByRegistrationNumber(self, registrationNumber):
        try:
            _id = self.getRecipe_id(registrationNumber)
        except ValueError as err:
            raise err
        except RuntimeError as err:
            raise err

        return self.Recipes.find_one({'_id': _id})

    def getRecipeBy_id(self, _id):
        recipe = self.Recipes.find_one({'_id': _id})

        if recipe is None:
            raise ValueError('Impossível encontrar receita _id: ' + str(_id))

        return recipe

    def getRecipeCursorByTermSimilarity(self, term):
        # Gera uma lista de palavras para procurar todos os termos
        searchableTermsList = [self.getSimilaritySearchableRegex(item)
                               for item in term.split()]

        recipesCursor = self.Recipes.find(
            {'$or': [
                    {'petSearchable': {'$in': searchableTermsList}},
                    {'tutorSearchable': {'$in': searchableTermsList}},
                    {'nutricionistSeachable': {'$in': searchableTermsList}},
                    {'recipeNameSearchable': {'$in': searchableTermsList}},
                    {'registrationNumber': {'$in': searchableTermsList}}
                ]
             }
        ).sort('date', 1)

        return recipesCursor

    def removeRecipe(self, _id):
        result = self.Recipes.delete_one({'_id': _id})
        if result.deleted_count == 0:
            raise ValueError(
                'Não foi possível deletar o documento _id: ' + str(_id))

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
