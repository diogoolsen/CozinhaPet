
# import pytest
import datetime

from pytest import approx, raises

from src.model.ingredient import Ingredient


class TestIngredient():
    def assert_item_by_item(self, actual, expected, message=''):

        assert actual['name'] == expected['name'], message
        assert actual['searchable'] == expected['searchable'], message
        assert actual['type'] == expected['type'], message
        assert actual['unity'] == expected['unity'], message

        assert actual['establishedCostPer1K'] == \
            approx(expected['establishedCostPer1K'])

        assert isinstance(actual['factorsLog'][0]['date'],
                          datetime.datetime)
        assert actual['factorsLog'][0]['cookingFactor'] ==\
            approx(expected['factorsLog'][0]['cookingFactor']), message
        assert actual['factorsLog'][0]['safetyMargin'] ==\
            approx(expected['factorsLog'][0]['safetyMargin']), message
        assert actual['factorsLog'][0]['actualFactor'] ==\
            approx(expected['factorsLog'][0]['actualFactor']), message

        assert isinstance(actual['costLog'][0]['date'],
                          datetime.datetime)
        assert actual['costLog'][0]['price'] ==\
            approx(expected['costLog'][0]['price']), message
        assert actual['costLog'][0]['amount'] ==\
            approx(expected['costLog'][0]['amount']), message
        assert actual['costLog'][0]['costPer1Unity'] ==\
            approx(expected['costLog'][0]['costPer1Unity']), message
        assert actual['costLog'][0]['costPer1K'] ==\
            approx(expected['costLog'][0]['costPer1K']), message

    def test_create_ingredient_OK_v1(self):

        name = 'abobrinha'
        type = 'vegetal'
        unity = 'g'
        price = '3.14'
        established = '3'

        actual = Ingredient(name, type, unity, price, established).dict

        expected_factors_dict = {
            'date': datetime.datetime.now(),
            'cookingFactor': 1.,
            'safetyMargin': 1.,
            'actualFactor': 1.
        }

        expected_cost_dict = {
            'date': datetime.datetime.now(),
            'price': 3.14,
            'amount': 1000.,
            'costPer1Unity': 0.00314,
            'costPer1K': 3.14
        }

        expected = {
            'name': 'abobrinha',
            'searchable': 'ABOBRINHA',
            'type': 'vegetal',
            'unity': 'g',
            # 'amount': 1000.,
            'factorsLog': [expected_factors_dict],
            'costLog': [expected_cost_dict],
            'establishedCostPer1K': 3.
        }

        message = ('test_create_ingredient_OK_v1 returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        self.assert_item_by_item(actual, expected, message)

    def test_create_ingredient_OK_v2(self):

        name = 'figado bovino'
        type = 'carne'
        unity = 'g'
        price = '32.5'
        established = '65'
        amount = '500'
        cookingFactor = '0.75'
        safetyMargin = '1.05'

        actual = Ingredient(name,
                            type,
                            unity,
                            price,
                            established,
                            amount,
                            cookingFactor,
                            safetyMargin).dict

        expected_factors_dict = {
            'date': datetime.datetime.now(),
            'cookingFactor': 0.75,
            'safetyMargin': 1.05,
            'actualFactor': 0.7875
        }

        expected_cost_dict = {
            'date': datetime.datetime.now(),
            'price': 32.5,
            'amount': 500.,
            'costPer1Unity': 0.065,
            'costPer1K': 65
        }

        expected = {
            'name': 'figado bovino',
            'searchable': 'FIGADO BOVINO',
            'type': 'carne',
            'unity': 'g',
            # 'amount': 500.,
            'factorsLog': [expected_factors_dict],
            'costLog': [expected_cost_dict],
            'establishedCostPer1K': 65
        }

        message = ('test_create_ingredient_OK_v2 returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        self.assert_item_by_item(actual, expected, message)

    def test_create_ingredient_validate_v1(self):

        name = ''
        type = 'complemento'
        unity = 'ml'
        price = '32'
        established = '32'

        with raises(ValueError) as exception_info:
            # store the exception
            Ingredient(name, type, unity, price, established)

        # Check if ValueError contains correct message
        assert exception_info.match('Nome do ingrediente inválido.')

    def test_create_ingredient_validate_v2(self):

        name = 'Óleo de coco'
        type = ''
        unity = 'ml'
        price = '32'
        established = '64'

        with raises(ValueError) as exception_info:
            # store the exception
            Ingredient(name, type, unity, price, established)

        # Check if ValueError contains correct message
        assert exception_info.match('Tipo do ingrediente inválido.')

    def test_create_ingredient_validate_v3(self):

        name = 'Óleo de coco'
        type = 'complemento'
        unity = ''
        price = '32'
        established = '64'

        with raises(ValueError) as exception_info:
            # store the exception
            Ingredient(name, type, unity, price, established)

        # Check if ValueError contains correct message
        assert exception_info.match('Unidade do ingrediente inválido')

    def test_create_ingredient_validate_v4(self):

        name = 'Óleo de coco'
        type = 'complemento'
        unity = 'ml'
        price = '32,5'
        established = '65'

        with raises(ValueError) as exception_info:
            # store the exception
            Ingredient(name, type, unity, price, established)

        # Check if ValueError contains correct message
        assert exception_info.match('Custo do ingrediente inválido.')

    def test_create_ingredient_validate_v5(self):

        name = 'Óleo de coco'
        type = 'complemento'
        unity = 'ml'
        price = '32'
        established = '64'
        amount = '22x'

        with raises(ValueError) as exception_info:
            # store the exception
            Ingredient(name, type, unity, price, established, amount)

        # Check if ValueError contains correct message
        assert exception_info.match('Quantidade de ingrediente inválida.')

    def test_create_ingredient_validate_v6(self):

        name = 'Óleo de coco'
        type = 'complemento'
        unity = 'ml'
        price = '32'
        established = '64'
        amount = '22'
        cookingFactor = '1,2'
        safetyMargin = '1.1'

        with raises(ValueError) as exception_info:
            # store the exception
            Ingredient(name, type, unity, price, established, amount,
                       cookingFactor, safetyMargin)

        # Check if ValueError contains correct message
        assert exception_info.match('Fator de cocção do ingrediente inválido.')

    def test_create_ingredient_validate_v7(self):

        name = 'Óleo de coco'
        type = 'complemento'
        unity = 'ml'
        price = '32'
        established = '64'
        amount = '22'
        cookingFactor = '1.2'
        safetyMargin = '1,1'

        with raises(ValueError) as exception_info:
            # store the exception
            Ingredient(name, type, unity, price, established, amount,
                       cookingFactor, safetyMargin)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'Margem de segurança do ingrediente inválida.')
