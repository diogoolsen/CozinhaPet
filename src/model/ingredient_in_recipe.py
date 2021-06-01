

class IngredientInRecipe():

    def __init__(self, ingredientDict, newestActualFactor, dailyAmount):

        try:
            self.validate(ingredientDict, newestActualFactor, dailyAmount)
        except ValueError as err:
            raise err

        self.dict = {
            'ingredient_id': ingredientDict['_id'],
            'name': ingredientDict['name'],
            'searchable': ingredientDict['searchable'],
            'type': ingredientDict['type'],
            'unity': ingredientDict['unity'],
            'currentActualCookingFactor': newestActualFactor,
            'establishedCostPer1K': ingredientDict['establishedCostPer1K'],
            'dailyAmount': dailyAmount
        }

    def validate(self, ingredientDict, newestActualFactor, dailyAmount):

        necessaryFields = ['name',
                           'searchable',
                           'type',
                           'unity',
                           'establishedCostPer1K']

        try:
            # Verifica se o dicionário possui todos os campos necessários
            #
            # Se não tiver vai provocar um KeyError
            checkAllFields = [
                # Vai inserir 'NoData' em uma lista
                'NoData'
                # Ao iterar sobre a lista de campos necessários
                for field in necessaryFields
                # Quando um valor for nulo
                if ingredientDict[field] == '']
        except KeyError:
            raise ValueError(
                'O dicionário não possui todos os campos necessários')
        else:
            # Verifica se o dicionário possui todos os valores necessários
            if 'NoData' in checkAllFields:
                raise ValueError(
                    'O dicionário não possui todos os valores necessários')

        try:
            newestActualFactor = float(newestActualFactor)
        except ValueError:
            raise ValueError('Fator atual do ingrediente inválido: '
                             + str(newestActualFactor))

        try:
            dailyAmount = float(dailyAmount)
        except ValueError:
            raise ValueError('Quantidade diária do ingrediente inválida: '
                             + str(dailyAmount))
