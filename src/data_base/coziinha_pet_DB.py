
from pymongo import MongoClient


class CozinhaPetDB():

    def __init__(self):

        # Client connects to "localhost" by default
        self.client = MongoClient()

        # Create local 'CozinhaPetDB' database on the fly
        # Acessa o banco de dados 'CozinhaPetDB'
        self.CozinhaPetDB = self.client.CozinhaPetDB

        # Acessa a coleção 'Ingredientes'
        self.Ingredientes = self.CozinhaPetDB.Ingredientes

    def getAll(self):
        return self.Ingredientes.find()

    def getIngredientByName(self, name):
        return self.Ingredientes.find_one({'name': name})

    def addIngredient(self, dict):
        # Verificar se já não está no banco
        if self.Ingredientes.find_one({'name': dict['name']}):
            raise ValueError('Item já cadastrado.')
        else:
            self.Ingredientes.insert_one(dict)

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
