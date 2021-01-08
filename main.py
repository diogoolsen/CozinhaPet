
from src.model.ingredient import Ingredient
from src.data_base.coziinha_pet_DB import CozinhaPetDB


ingredient = Ingredient('abobrinha',
                        'vegetal',
                        'g',
                        '3.14')

# print(ingredient.dict['name'])
# print(ingredient.dict)

DB = CozinhaPetDB()
# DB.addIngredient(ingredient.dict)

item = DB.getIngredientByName('abobrinha')
print(item)


# name: str,
# type: str,     # meat, vegetable, supplement
# unity: str,    # g, ml, undefined (if supplement)
# price: str,
# amount: str = '1000',
# cookingFactor: str = '1.'',
# safetyMargin: str = '1.'

# class Erro():
#     def __init__(self):
#         raise ValueError('class <' + self.__class__.__qualname__ +
#                          '> - Erro')
#         return 10


# def cria(a):
#     try:
#         a += Erro()
#     except ValueError as Error:
#         raise Error
#         a = 15
#         print('erro tratado')

#     a += Erro()

#     print(a)
#     return a


# try:
#     x = cria(10)
# except ValueError as identifier:
#     print(' -> ', type(identifier))
#     print(' -> ', identifier)
#     x = 0

# print(x)

# cria(10)
