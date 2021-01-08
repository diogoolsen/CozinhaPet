
import datetime

from pytest import approx, raises

from src.model.factors_item import FactorsItem


class TestFactorsItem():
    def assert_item_by_item(self, actual, expected, message=''):

        assert isinstance(actual['date'], datetime.datetime)
        assert actual['cookingFactor'] == approx(
            expected['cookingFactor']), message
        assert actual['safetyMargin'] == approx(
            expected['safetyMargin']), message
        assert actual['actualFactor'] == approx(
            expected['actualFactor']), message

    def test_create_factors_item_bad_cookingFactor_v1(self):

        cookingFactor = '-1.1'
        safetyMargin = '1.05'

        with raises(ValueError) as exception_info:
            # store the exception
            FactorsItem(cookingFactor, safetyMargin)

        # Check if ValueError contains correct message
        assert exception_info.match('Fator de cocção do ingrediente inválido.')

    def test_create_factors_item_bad_cookingFactor_v2(self):

        cookingFactor = '1.1z'
        safetyMargin = '1.05'

        with raises(ValueError) as exception_info:
            # store the exception
            FactorsItem(cookingFactor, safetyMargin)

        # Check if ValueError contains correct message
        assert exception_info.match('Fator de cocção do ingrediente inválido.')

    def test_create_factors_item_bad_cookingFactor_v3(self):

        cookingFactor = '1,1'
        safetyMargin = '1.05'

        with raises(ValueError) as exception_info:
            # store the exception
            FactorsItem(cookingFactor, safetyMargin)

        # Check if ValueError contains correct message
        assert exception_info.match('Fator de cocção do ingrediente inválido.')

    def test_create_factors_item_bad_safetyMargin_v1(self):

        cookingFactor = '1.1'
        safetyMargin = '-1.05'

        with raises(ValueError) as exception_info:
            # store the exception
            FactorsItem(cookingFactor, safetyMargin)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'Margem de segurança do ingrediente inválida.')

    def test_create_factors_item_bad_safetyMargin_v2(self):

        cookingFactor = '1.1'
        safetyMargin = '1,05'

        with raises(ValueError) as exception_info:
            # store the exception
            FactorsItem(cookingFactor, safetyMargin)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'Margem de segurança do ingrediente inválida.')

    def test_create_factors_item_bad_safetyMargin_v3(self):

        cookingFactor = '1.1'
        safetyMargin = '1.05z'

        with raises(ValueError) as exception_info:
            # store the exception
            FactorsItem(cookingFactor, safetyMargin)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'Margem de segurança do ingrediente inválida.')

    def test_create_factors_item_bad_date_v1(self):

        cookingFactor = '1.1'
        safetyMargin = '1.05'

        with raises(ValueError) as exception_info:
            # store the exception
            FactorsItem(cookingFactor, safetyMargin, '2021/01/06')

        # Check if ValueError contains correct message
        assert exception_info.match(
            'Data dos fatores do ingrediente inválida.')

    def test_create_factors_item_bad_date_v2(self):

        cookingFactor = '1.1'
        safetyMargin = '1.05'

        with raises(ValueError) as exception_info:
            # store the exception
            FactorsItem(cookingFactor, safetyMargin, 10)

        # Check if ValueError contains correct message
        assert exception_info.match(
            'Data dos fatores do ingrediente inválida.')

    def test_create_factors_item_float_data(self):

        cookingFactor = 0.75
        safetyMargin = 1.05

        actual = FactorsItem(cookingFactor, safetyMargin).dict

        expected = {
            'date': datetime.datetime.now(),
            'cookingFactor': float(cookingFactor),
            'safetyMargin': float(safetyMargin),
            'actualFactor': 0.7875
        }

        message = ('test_create_factors_item_float_data returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        self.assert_item_by_item(actual, expected, message)

    def test_create_factors_item_str_data(self):

        cookingFactor = '0.75'
        safetyMargin = '1.05'

        actual = FactorsItem(cookingFactor, safetyMargin).dict

        expected = {
            'date': datetime.datetime.now(),
            'cookingFactor': float(cookingFactor),
            'safetyMargin': float(safetyMargin),
            'actualFactor': 0.7875
        }

        message = ('test_create_factors_item_str_data returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        self.assert_item_by_item(actual, expected, message)

    def test_create_factors_item_v1(self):

        cookingFactor = '0.75'
        safetyMargin = '1.'

        actual = FactorsItem(cookingFactor, safetyMargin).dict

        expected = {
            'date': datetime.datetime.now(),
            'cookingFactor': float(cookingFactor),
            'safetyMargin': float(safetyMargin),
            'actualFactor': 0.75
        }

        message = ('test_create_factors_item_v1 returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        self.assert_item_by_item(actual, expected, message)

    def test_create_factors_item_v2(self):

        cookingFactor = '1.5'
        safetyMargin = '1.05'

        actual = FactorsItem(cookingFactor, safetyMargin).dict

        expected = {
            'date': datetime.datetime.now(),
            'cookingFactor': float(cookingFactor),
            'safetyMargin': float(safetyMargin),
            'actualFactor': 1.575
        }

        message = ('test_create_factors_item_v2 returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        self.assert_item_by_item(actual, expected, message)

    def test_create_factors_item_v3(self):

        cookingFactor = '0.75'
        safetyMargin = '1.05'
        date = datetime.datetime.now()

        actual = FactorsItem(cookingFactor, safetyMargin, date).dict

        expected = {
            'date': date,
            'cookingFactor': float(cookingFactor),
            'safetyMargin': float(safetyMargin),
            'actualFactor': 0.7875
        }

        message = ('test_create_factors_item_v3 returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )
        assert actual['date'] == expected['date'], message

        self.assert_item_by_item(actual, expected, message)

    def test_create_factors_item_v4(self):

        cookingFactor = '0.75'
        safetyMargin = '1.05'

        actual = FactorsItem(cookingFactor, safetyMargin, None).dict

        expected = {
            'date': datetime.datetime.now(),
            'cookingFactor': float(cookingFactor),
            'safetyMargin': float(safetyMargin),
            'actualFactor': 0.7875
        }

        message = ('test_create_factors_item_v4 returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        self.assert_item_by_item(actual, expected, message)
