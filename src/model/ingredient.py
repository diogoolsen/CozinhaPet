
from datetime import date


class Ingredient():
    def __init__(self,
                 name: str,
                 type: str,     # meat, vegetable, supplement
                 unity: str,    # g, ml, undefined (if supplement)
                 cookingFactor: float = 1.,
                 safetyMargin: float = 1.,
                 stockLog: bool = False) -> None:

        # Validate
        if name == '':
            raise ValueError(
                'ingredient.py->Ingredient->__init__ - '
                'Nome do ingrediente inválido')

        if type == '':
            raise ValueError(
                'ingredient.py->Ingredient->__init__ - '
                'Nome do tipo inválido')

        if unity == '':
            raise ValueError(
                'ingredient.py->Ingredient->__init__ - '
                'Unidade do ingrediente inválido')

        # if cost == '':
        #     raise ValueError(
        #         'ingredient.py->Ingredient->__init__ - '
        #         'Custo do ingrediente inválido')

        # try:
        #     float(cost)
        # except ValueError:
        #     raise ValueError(
        #         'ingredient.py->Ingredient->__init__ - '
        #         'Custo do ingrediente inválido - não é formato numérico')

        # costPer1Unity = (float(cost) / float(amount))

        # if costDate is None:
        #     costDate = date.today()

        # cost_dict = {
        #     'costPer1Unity': costPer1Unity,
        #     'date': costDate
        # }

        factors_list = {
            'date': date.today(),
            'cookingFactor': cookingFactor,
            'safetyMargin': safetyMargin,
            'actualFactor': cookingFactor * safetyMargin
        }

        self.ingredient = {
            'name': name,
            'type': type,
            'unity': unity,
            'cookingFactor': cookingFactor,
            'safetyMargin': safetyMargin,
            'costLog': [factors_list]
        }

    def getDict(self):
        return self.ingredient

    def generateBSON(self):
        pass

    def getCost(self):
        pass

    def convertML4G(self):
        pass
