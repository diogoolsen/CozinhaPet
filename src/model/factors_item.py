
import datetime


class FactorsItem():

    def __init__(self, cookingFactor, safetyMargin, factorsDate=None):

        try:
            self.validate(cookingFactor, safetyMargin, factorsDate)
        except ValueError as Error:
            raise Error

        actualFactor = float(cookingFactor) * float(safetyMargin)

        if factorsDate is None:
            date = datetime.datetime.now()
        else:
            date = factorsDate

        self.dict = {
            'date': date,
            'cookingFactor': float(cookingFactor),
            'safetyMargin': float(safetyMargin),
            'actualFactor': actualFactor
        }

    def validate(self, cookingFactor, safetyMargin, factorsDate=None):

        try:
            float(cookingFactor)
        except ValueError:
            raise ValueError('Fator de cocção do ingrediente inválido.')

        if float(cookingFactor) < 0:
            raise ValueError('Fator de cocção do ingrediente inválido.')

        try:
            float(safetyMargin)
        except ValueError:
            raise ValueError('Margem de segurança do ingrediente inválida.')

        if float(safetyMargin) < 0:
            raise ValueError('Margem de segurança do ingrediente inválida.')

        if factorsDate is None:
            pass
        elif not isinstance(factorsDate, datetime.datetime):
            raise ValueError('Data dos fatores do ingrediente inválida.')
