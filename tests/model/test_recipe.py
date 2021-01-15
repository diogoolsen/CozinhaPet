# import pytest
import datetime

from pytest import raises

from src.model.recipe import Recipe


class TestRecipe():
    def assert_item_by_item(self, actual, expected, message=''):

        assert actual['petName'] == expected['petName'], message
        assert actual['petSearchable'] == expected['petSearchable'], message
        assert actual['tutorName'] == expected['tutorName'], message
        assert actual['tutorSearchable'] ==\
            expected['tutorSearchable'], message
        assert actual['nutricionistName'] ==\
            expected['nutricionistName'], message
        assert actual['nutricionistSeachable'] ==\
            expected['nutricionistSeachable'], message
        assert actual['recipeName'] == expected['recipeName'], message
        assert actual['recipeNameSearchable'] ==\
            expected['recipeNameSearchable'], message

        assert isinstance(actual['date'], datetime.datetime)
        assert isinstance(actual['ingredientsRecipeList'], list)

    def test_create_recipe_OK_v1(self):

        expected = {
            'petName': 'Ozzy Osbourne',
            'petSearchable': 'OZZY OSBOURNE',
            'tutorName': 'Diogo Olsen',
            'tutorSearchable': 'DIOGO OLSEN',
            'nutricionistName': 'Káçia Menolli',
            'nutricionistSeachable': 'KACIA MENOLLI',
            'recipeName': 'Frango e Bacon',
            'recipeNameSearchable': 'FRANGO E BACON',
            # 'registrationNumber': '1',
            'date': datetime.datetime.now(),
            'ingredientsRecipeList': []
        }

        actual = Recipe(expected['petName'],
                        expected['tutorName'],
                        expected['nutricionistName'],
                        expected['recipeName'])

        self.assert_item_by_item(actual.dict, expected)

    def test_create_recipe_OK_v2(self):

        expected = {
            'petName': 'Bruce Wayne',
            'petSearchable': 'BRUCE WAYNE',
            'tutorName': 'Márcela Baggio',
            'tutorSearchable': 'MARCELA BAGGIO',
            'nutricionistName': 'Luçiana Pereira',
            'nutricionistSeachable': 'LUCIANA PEREIRA',
            'recipeName': 'Arroz Com Carne Moída',
            'recipeNameSearchable': 'ARROZ COM CARNE MOIDA',
            # 'registrationNumber': '1',
            'date': datetime.datetime.now(),
            'ingredientsRecipeList': []
        }

        actual = Recipe(expected['petName'],
                        expected['tutorName'],
                        expected['nutricionistName'],
                        expected['recipeName'])

        self.assert_item_by_item(actual.dict, expected)

    def test_create_recipe_Bad_petName(self):

        with raises(ValueError) as exception_info:
            # store the exception
            Recipe('',
                   'Diogo Olsen',
                   'Kássia Menolli',
                   'Arroz com Frango')

        # Check if ValueError contains correct message
        assert exception_info.match('Nome do pet inválido.')

    def test_create_recipe_Bad_tutorName(self):

        with raises(ValueError) as exception_info:
            # store the exception
            Recipe('Ozzy Osbourne',
                   '',
                   'Kássia Menolli',
                   'Arroz com Frango')

        # Check if ValueError contains correct message
        assert exception_info.match('Nome do tutor inválido.')

    def test_create_recipe_Bad_nutricionistName(self):

        with raises(ValueError) as exception_info:
            # store the exception
            Recipe('Ozzy Osbourne',
                   'Diogo Olsen',
                   '',
                   'Arroz com Frango')

        # Check if ValueError contains correct message
        assert exception_info.match('Nome do nutricionista inválido.')

    def test_create_recipe_Bad_recipeName(self):

        with raises(ValueError) as exception_info:
            # store the exception
            Recipe('Ozzy Osbourne',
                   'Diogo Olsen',
                   'Kássia Menolli',
                   '')

        # Check if ValueError contains correct message
        assert exception_info.match('Nome da receita inválido.')
