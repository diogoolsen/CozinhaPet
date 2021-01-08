
# import pytest
from datetime import date

from pytest import approx, raises

from src.model.ingredient import Ingredient


class Test_Ingredient():
    def test_create_ingredient_v1(self):

        name = 'abobrinha'
        type = 'vegetal'
        cost = '3.14'
        unity = 'Kg'

        actual = Ingredient(name, type, cost, unity).getDict()

        cost_dict = {
            'costPer1Unity': 0.00314,
            'date': date.today()
        }

        expected = {
            'name': 'abobrinha',
            'type': 'vegetal',
            'unity': 'Kg',
            'amount': 1000.,
            'cookingFactor': 1.,
            'safetyMargin': 1.,
            'costLog': [cost_dict]
        }

        message = ('test_create_ingredient returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        print(actual)
        assert actual['name'] == expected['name'], message
        assert actual['type'] == expected['type'], message
        assert actual['unity'] == expected['unity'], message
        assert actual['amount'] == expected['amount'], message
        assert actual['cookingFactor'] == expected['cookingFactor'], message
        assert actual['safetyMargin'] == expected['safetyMargin'], message
        assert actual['costLog'][0]['costPer1Unity'] ==\
            approx(expected['costLog'][0]['costPer1Unity']), message
        assert actual['costLog'][0]['date'] ==\
            expected['costLog'][0]['date'], message

    def test_create_ingredient_v2(self):

        name = 'Fígado Bovino'
        type = 'carne'
        cost = '32.99'
        unity = 'Kg'

        actual = Ingredient(name,
                            type,
                            cost,
                            unity,
                            cookingFactor=0.78,
                            safetyMargin=1.05).getDict()

        cost_dict = {
            'costPer1Unity': 0.03299,
            'date': date.today()
        }

        expected = {
            'name': 'Fígado Bovino',
            'type': 'carne',
            'unity': 'Kg',
            'cookingFactor': 0.78,
            'safetyMargin': 1.05,
            'costLog': [cost_dict]
        }

        message = ('test_create_ingredient returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        print(actual)
        assert actual['name'] == expected['name'], message
        assert actual['type'] == expected['type'], message
        assert actual['unity'] == expected['unity'], message
        assert actual['cookingFactor'] == expected['cookingFactor'], message
        assert actual['safetyMargin'] == expected['safetyMargin'], message
        assert actual['costLog'][0]['costPer1Unity'] == \
            approx(expected['costLog'][0]['costPer1Unity']), message
        assert actual['costLog'][0]['date'] ==\
            expected['costLog'][0]['date'], message

    def test_create_ingredient_v3(self):

        name = 'Óleo de Coco'
        type = 'complemento'
        cost = '32'
        unity = 'ml'

        actual = Ingredient(name,
                            type,
                            cost,
                            unity,
                            amount=500).getDict()

        cost_dict = {
            'costPer1Unity': 0.064,
            'date': date.today()
        }

        expected = {
            'name': 'Óleo de Coco',
            'type': 'complemento',
            'unity': 'ml',
            'cookingFactor': 1,
            'safetyMargin': 1,
            'costLog': [cost_dict]
        }

        message = ('test_create_ingredient returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        print(actual)
        assert actual['name'] == expected['name'], message
        assert actual['type'] == expected['type'], message
        assert actual['unity'] == expected['unity'], message
        assert actual['cookingFactor'] == expected['cookingFactor'], message
        assert actual['safetyMargin'] == expected['safetyMargin'], message
        assert actual['costLog'][0]['costPer1Unity'] == \
            approx(expected['costLog'][0]['costPer1Unity']), message
        assert actual['costLog'][0]['date'] ==\
            expected['costLog'][0]['date'], message

    def test_create_ingredient_v4(self):

        type = 'complemento'
        cost = '32'
        unity = 'ml'

        with raises(ValueError) as exception_info:
            # store the exception
            Ingredient('', type, cost, unity)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'ingredient.py->Ingredient->__init__ - '
            'Nome do ingrediente inválido')

    def test_create_ingredient_v5(self):

        name = 'Óleo de coco'
        cost = '32'
        unity = 'ml'

        with raises(ValueError) as exception_info:
            # store the exception
            Ingredient(name, '', cost, unity)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'ingredient.py->Ingredient->__init__ - '
            'Nome do tipo inválido')

    def test_create_ingredient_v6(self):

        name = 'Óleo de coco'
        type = 'complemento'
        unity = 'ml'

        with raises(ValueError) as exception_info:
            # store the exception
            Ingredient(name, type, '', unity)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'ingredient.py->Ingredient->__init__ - '
            'Custo do ingrediente inválido')

    def test_create_ingredient_v7(self):

        name = 'Óleo de coco'
        type = 'complemento'
        cost = '32'

        with raises(ValueError) as exception_info:
            # store the exception
            Ingredient(name, type, cost, '')

        # Check if ValueError contains correct message
        assert exception_info.match(
            'ingredient.py->Ingredient->__init__ - '
            'Unidade do ingrediente inválido')

    def test_create_ingredient_v8(self):

        name = 'Óleo de coco'
        type = 'complemento'
        unity = 'ml'

        with raises(ValueError) as exception_info:
            # store the exception
            Ingredient(name, type, '32x', unity)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'ingredient.py->Ingredient->__init__ - '
            'Custo do ingrediente inválido - não é formato numérico')
