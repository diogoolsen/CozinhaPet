
import datetime

import unidecode


class Recipe():
    def __init__(self,
                 pet: str,
                 tutor: str,
                 nutricionist: str,
                 recipeName: str) -> None:

        try:
            self.validate(pet, tutor, nutricionist, recipeName)
        except ValueError as Error:
            raise Error

        self.dict = {
            'petName': pet,
            'petSearchable': unidecode.unidecode(pet).upper(),
            'tutorName': tutor,
            'tutorSearchable': unidecode.unidecode(tutor).upper(),
            'nutricionistName': nutricionist,
            'nutricionistSeachable': unidecode.unidecode(nutricionist).upper(),
            'recipeName': recipeName,
            'recipeNameSearchable': unidecode.unidecode(recipeName).upper(),
            'registrationNumber': -1,
            'date': datetime.datetime.now(),
            'ingredientsRecipeList': []
        }

    def validate(self, pet, tutor, nutricionist, recipeName):

        if pet == '':
            raise ValueError('Nome do pet inválido.')

        if tutor == '':
            raise ValueError('Nome do tutor inválido.')

        if nutricionist == '':
            raise ValueError('Nome do nutricionista inválido.')

        if recipeName == '':
            raise ValueError('Nome da receita inválido.')
