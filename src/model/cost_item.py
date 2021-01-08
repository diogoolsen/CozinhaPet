
import datetime


class CostItem():

    def __init__(self, price, amount, costDate=None):

        try:
            self.validate(price, amount, costDate)
        except ValueError as Error:
            raise Error

        costPer1Unity = float(float(price) / float(amount))
        costPer1k = float(costPer1Unity * 1000)

        if costDate is None:
            date = datetime.datetime.now()
        else:
            date = costDate

        self.dict = {
            'date': date,
            'price': float(price),
            'amount': float(amount),
            'costPer1Unity': costPer1Unity,
            'costPer1K': costPer1k
        }

    def validate(self, price, amount, costDate=None):

        try:
            float(price)
        except ValueError:
            raise ValueError('Custo do ingrediente inválido.')

        if float(price) < 0:
            raise ValueError('Custo do ingrediente inválido.')

        try:
            float(amount)
        except ValueError:
            raise ValueError('Quantidade de ingrediente inválida.')

        if float(amount) < 0:
            raise ValueError('Quantidade de ingrediente inválida.')

        if costDate is None:
            pass
        elif not isinstance(costDate, datetime.datetime):
            raise ValueError('Data do custo do ingrediente inválida.')
