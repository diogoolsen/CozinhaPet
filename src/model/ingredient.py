
from src.model.cost_item import CostItem
from src.model.factors_item import FactorsItem


class Ingredient():
    def __init__(self,
                 name: str,
                 type: str,     # meat, vegetable, supplement
                 unity: str,    # g, ml, undefined (if supplement)
                 price: str,
                 amount: str = '1000',
                 cookingFactor: str = '1.',
                 safetyMargin: str = '1.') -> None:

        try:
            self.validate(name, type, unity)

            costItem = CostItem(price, amount)
            factorsItem = FactorsItem(cookingFactor, safetyMargin)
        except ValueError as Error:
            raise Error

        self.dict = {
            'name': name,
            'type': type,
            'unity': unity,
            'factorsLog': [factorsItem.dict],
            'costLog': [costItem.dict]
            # 'stockLog': False,      # True\False
            # 'stock': [stock_list]
        }

    def validate(self, name, type, unity):

        if name == '':
            raise ValueError('Nome do ingrediente inválido.')

        if type == '':
            raise ValueError('Tipo do ingrediente inválido.')

        if unity == '':
            raise ValueError('Unidade do ingrediente inválido')

    # def generateBSON(self):
    #     pass

    # def getCost(self):
    #     pass

    # def convertML4G(self):
    #     pass
