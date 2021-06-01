
from pymongo.collection import ReturnDocument

from src.model import Recipe, IngredientInRecipe
from src.data_base.mongo_database import MongoDataBase


class RecipesDB(MongoDataBase):

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

    def isRecipeInDB(self, _id):
        recipe = self.Recipes.find_one({'_id': _id})

        if recipe is None:
            raise ValueError('Impossível encontrar receita _id: ' + str(_id))

        return True

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

    def getRecipeCursorByTermSimilarity(self, term: str):
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

    #
    # Testado até aqui!
    #

    #
    # Manipulate Ingredients In Recipe
    #

    # def findIngredientInRecipe(self, recipe_id, ingredient_id):
    #     ingredient = self.Recipes.find_one(
    #             {'_id': recipe_id,
    #              'ingredientsRecipeList.ingredient_id': ingredient_id
    #              }
    #         )

    #     if ingredient is None:
    #         raise ValueError('Ingrediente não encontrado na receita')

    #     return ingredient

    def isIngredientInRecipe(self, recipe_id, ingredient_id):
        ingredient = self.Recipes.find_one(
            {'_id': recipe_id,
             'ingredientsRecipeList.ingredient_id': ingredient_id
             }
        )

        if ingredient is None:
            return False
        else:
            return True

    def addIngredientToRecipe(self, recipe_id, ingredientInRecipe):
        try:
            self.isRecipeInDB(recipe_id)
        except ValueError as err:
            raise err

        if not isinstance(ingredientInRecipe, IngredientInRecipe):
            raise ValueError(
                'Tipo de dado do ingrediente da receita inválido.')

        if self.isIngredientInRecipe(
                recipe_id,
                ingredientInRecipe.dict['ingredient_id']):

            raise ValueError('Ingrediente já inserido na receita - '
                             'Atualize seu valor.')

        result = self.Recipes.update_one(
            {'_id': recipe_id},
            {'$push': {'ingredientsRecipeList': ingredientInRecipe.dict}}
        )

        if result.modified_count != 1:
            raise RuntimeError('Ingrediente não atualizado!')

    def remIngredientFromRecipe(self, recipe_id, ingredient_id):
        try:
            self.isRecipeInDB(recipe_id)
        except ValueError as err:
            raise err

        if not self.isIngredientInRecipe(recipe_id, ingredient_id):
            raise ValueError('Ingrediente não inserido na receita.')

        result = self.Recipes.update_one(
            {'_id': recipe_id},
            {'$pull': {
                'ingredientsRecipeList': {'ingredient_id': ingredient_id}
            }}
        )

        #
        # Verificar se esta operação não está removendo ou
        #  - todos os itens com o mesmo id desta receita
        #  - todos os itens com o mesmo id de qualquer receita
        #

        if result.modified_count != 1:
            raise RuntimeError('Ingrediente não atualizado!' + str(result))

    def getIngredientsListFromRecipe(self, recipe_id):
        try:
            self.isRecipeInDB(recipe_id)
        except ValueError as err:
            raise err

        ingredientsList = self.Recipes.find_one(
            {'_id': recipe_id},
            {'_id': 0, 'ingredientsRecipeList': 1}
        )

        if ingredientsList is None:
            raise RuntimeError('Impossível encontrar lista.')

        return ingredientsList['ingredientsRecipeList']
