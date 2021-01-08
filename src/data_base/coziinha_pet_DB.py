
from pymongo import MongoClient


class CozinhaPetDB():
    def __init__(self):

        # Client connects to "localhost" by default
        self.client = MongoClient()

        # Create local "nobel" database on the fly
        # Acessa o banco de dados nobel
        self.CozinhaPetDB = self.client.CozinhaPetDB

        # Acessa a coleção prizes
        self.Ingredientes = self.CozinhaPetDB.Ingredientes

    def addIngredient(self, ingredient):
        # Verificar se já não está no banco
        pass

    def getIngredient_id(self, name):
        pass

    def addNewCost(self, _id, cost, inBulk=True):
        pass

    def updateStock(self, _id, amount, inBulk=True):
        pass

    def getNewestCost(self, _id):
        pass

    def getStockAmount(self, _id):
        pass
