
from src.model.ingredient import Ingredient
from src.data_base.cozinha_pet_DB import CozinhaPetDB


def populaDB():

    DB = CozinhaPetDB()

    ingredient = Ingredient('Abóbora Paulista',
                            'Vegetal',
                            'g',
                            '2',
                            cookingFactor='0.8',
                            safetyMargin='1.03')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Abobrinha',
                            'Vegetal',
                            'g',
                            '2.79',
                            cookingFactor='0.79',
                            safetyMargin='1.03')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Arroz integral',
                            'Vegetal',
                            'g',
                            '5.99',
                            cookingFactor='3.2',
                            safetyMargin='1.03')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Aveia em flocos',
                            'Vegetal',
                            'g',
                            '11',
                            cookingFactor='1',
                            safetyMargin='1')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Azeite de oliva extravirgem',
                            'Complemento',
                            'ml',
                            '42',
                            cookingFactor='1',
                            safetyMargin='1')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Batata doce',
                            'Vegetal',
                            'g',
                            '2.79',
                            cookingFactor='1.02',
                            safetyMargin='1.03')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Batata salsa',
                            'Vegetal',
                            'g',
                            '8',
                            cookingFactor='0.96',
                            safetyMargin='1')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Batata Yakon',
                            'Vegetal',
                            'g',
                            '10',
                            cookingFactor='0.9',
                            safetyMargin='1.03')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Cenoura',
                            'Vegetal',
                            'g',
                            '3.99',
                            cookingFactor='0.91',
                            safetyMargin='1.03')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Chuchu',
                            'Vegetal',
                            'g',
                            '3.79',
                            cookingFactor='0.79',
                            safetyMargin='1.03')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Couve',
                            'Vegetal',
                            'g',
                            '8.75',
                            cookingFactor='0.4',
                            safetyMargin='1.03')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Ervilha',
                            'Vegetal',
                            'g',
                            '20.96',
                            cookingFactor='0.95',
                            safetyMargin='1.03')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Farelo de aveia',
                            'Vegetal',
                            'g',
                            '9',
                            cookingFactor='1',
                            safetyMargin='1')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Fígado bovino',
                            'Carne',
                            'g',
                            '15.98',
                            cookingFactor='0.81',
                            safetyMargin='1.04')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Mignon suíno',
                            'Carne',
                            'g',
                            '21.9',
                            cookingFactor='0.69',
                            safetyMargin='1.04')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Músculo bovino',
                            'Carne',
                            'g',
                            '29.9',
                            cookingFactor='0.76',
                            safetyMargin='1.04')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Óleo de coco',
                            'Complemento',
                            'ml',
                            '64',
                            cookingFactor='1',
                            safetyMargin='1')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Óleo de Girassol prensado a frio',
                            'Complemento',
                            'ml',
                            '87.6',
                            cookingFactor='1',
                            safetyMargin='1')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Peito de frango',
                            'Carne',
                            'g',
                            '14.9',
                            cookingFactor='0.79',
                            safetyMargin='1.04')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Sal marinho',
                            'Complemento',
                            'g',
                            '3',
                            cookingFactor='1',
                            safetyMargin='1')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Tomate',
                            'Vegetal',
                            'g',
                            '7',
                            cookingFactor='0.95',
                            safetyMargin='1.03')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass

    ingredient = Ingredient('Vagem',
                            'Vegetal',
                            'g',
                            '6.59',
                            cookingFactor='0.86',
                            safetyMargin='1.03')

    try:
        DB.addIngredient(ingredient)
    except ValueError:
        pass


populaDB()
