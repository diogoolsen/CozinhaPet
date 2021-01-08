
# import pytest
import datetime

from pytest import approx, raises

from src.model.cost_item import CostItem


class TestCostItem():
    def assert_item_by_item(self, actual, expected, message=None):

        assert isinstance(actual['date'], datetime.datetime)
        assert actual['price'] == approx(expected['price']), message
        assert actual['amount'] == approx(expected['amount']), message
        assert actual['costPer1Unity'] == approx(
            expected['costPer1Unity']), message
        assert actual['costPer1K'] == approx(expected['costPer1K']), message

    def test_create_cost_item_bad_price_v1(self):

        price = '-31'
        amount = '1000.'

        with raises(ValueError) as exception_info:
            # store the exception
            CostItem(price, amount)

        # Check if ValueError contains correct message
        assert exception_info.match('Custo do ingrediente inválido.')

    def test_create_cost_item_bad_price_v2(self):

        price = '3,14'
        amount = '1000.'

        with raises(ValueError) as exception_info:
            # store the exception
            CostItem(price, amount)

        # Check if ValueError contains correct message
        assert exception_info.match('Custo do ingrediente inválido.')

    def test_create_cost_item_bad_price_v3(self):

        price = '3.14s'
        amount = '1000.'

        with raises(ValueError) as exception_info:
            # store the exception
            CostItem(price, amount)

        # Check if ValueError contains correct message
        assert exception_info.match('Custo do ingrediente inválido.')

    def test_create_cost_item_bad_amount_v1(self):

        price = '3.14'
        amount = '-1000.'

        with raises(ValueError) as exception_info:
            # store the exception
            CostItem(price, amount)

        # Check if ValueError contains correct message
        assert exception_info.match('Quantidade de ingrediente inválida.')

    def test_create_cost_item_bad_amount_v2(self):

        price = '3.14'
        amount = '1000,'

        with raises(ValueError) as exception_info:
            # store the exception
            CostItem(price, amount)

        # Check if ValueError contains correct message
        assert exception_info.match('Quantidade de ingrediente inválida.')

    def test_create_cost_item_bad_amount_v3(self):

        price = '3.14'
        amount = '1000.a'

        with raises(ValueError) as exception_info:
            # store the exception
            CostItem(price, amount)

        # Check if ValueError contains correct message
        assert exception_info.match('Quantidade de ingrediente inválida.')

    def test_create_cost_item_bad_date_v1(self):

        price = '3.14'
        amount = '1000.'

        with raises(ValueError) as exception_info:
            # store the exception
            CostItem(price, amount, '2021/061/06')

        # Check if ValueError contains correct message
        assert exception_info.match('Data do custo do ingrediente inválida.')

    def test_create_cost_item_bad_date_v2(self):

        price = '3.14'
        amount = '1000.'

        with raises(ValueError) as exception_info:
            # store the exception
            CostItem(price, amount, 10)

        # Check if ValueError contains correct message
        assert exception_info.match('Data do custo do ingrediente inválida.')

    def test_create_cost_item_float_data(self):

        price = 3.14
        amount = 1000.
        costPer1Unity = 0.00314
        costPer1k = 3.14

        actual = CostItem(price, amount).dict

        expected = {
            'date': datetime.datetime.now(),
            'price': float(price),
            'amount': float(amount),
            'costPer1Unity': costPer1Unity,
            'costPer1K': costPer1k
        }

        message = ('test_create_cost_item_float_data returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        self.assert_item_by_item(actual, expected, message)

    def test_create_cost_item_str_data(self):

        price = '3.14'
        amount = '1000.'
        costPer1Unity = 0.00314
        costPer1k = 3.14

        actual = CostItem(price, amount).dict

        expected = {
            'date': datetime.datetime.now(),
            'price': float(price),
            'amount': float(amount),
            'costPer1Unity': costPer1Unity,
            'costPer1K': costPer1k
        }

        message = ('test_create_cost_item_str_data returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        self.assert_item_by_item(actual, expected, message)

    def test_create_cost_item_v1(self):

        price = 7.
        amount = 500.
        costPer1Unity = 0.014
        costPer1k = 14.

        actual = CostItem(price, amount).dict

        expected = {
            'date': datetime.datetime.now(),
            'price': float(price),
            'amount': float(amount),
            'costPer1Unity': costPer1Unity,
            'costPer1K': costPer1k
        }

        message = ('test_create_cost_item_v1 returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        self.assert_item_by_item(actual, expected, message)

    def test_create_cost_item_v2(self):

        price = 1
        amount = 100.
        costPer1Unity = 0.01
        costPer1k = 10

        actual = CostItem(price, amount).dict

        expected = {
            'date': datetime.datetime.now(),
            'price': float(price),
            'amount': float(amount),
            'costPer1Unity': costPer1Unity,
            'costPer1K': costPer1k
        }

        message = ('test_create_cost_item_v2 returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        self.assert_item_by_item(actual, expected, message)

    def test_create_cost_item_v3(self):

        price = 7.
        amount = 500.
        costPer1Unity = 0.014
        costPer1k = 14.
        date = datetime.datetime.now()

        actual = CostItem(price, amount, date).dict

        expected = {
            'date': date,
            'price': float(price),
            'amount': float(amount),
            'costPer1Unity': costPer1Unity,
            'costPer1K': costPer1k
        }

        message = ('test_create_cost_item_v3 returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        assert actual['date'] == expected['date'], message

        self.assert_item_by_item(actual, expected, message)

    def test_create_cost_item_v4(self):

        price = 1
        amount = 100.
        costPer1Unity = 0.01
        costPer1k = 10

        actual = CostItem(price, amount, None).dict

        expected = {
            'date': datetime.datetime.now(),
            'price': float(price),
            'amount': float(amount),
            'costPer1Unity': costPer1Unity,
            'costPer1K': costPer1k
        }

        message = ('test_create_cost_item_v4 returned'
                   '{0}'
                   'instead of'
                   '{1}'.format(actual, expected)
                   )

        self.assert_item_by_item(actual, expected, message)
