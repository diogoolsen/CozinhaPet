
import re

import unidecode

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoDataBase():

    def __init__(self):

        try:
            # Client connects to "localhost" by default
            self.client = MongoClient()
        except ConnectionFailure:
            raise RuntimeError('Banco de Dados indisponível.')

        # Create local 'CozinhaPetDB' database on the fly
        # Acessa o banco de dados 'CozinhaPetDB'
        self.CozinhaPetDB = self.client.CozinhaPetDB

        # Acessa a coleção 'Ingredients'
        self.Ingredients = self.CozinhaPetDB.Ingredients

        # Acessa a coleção 'Recipes'
        self.Recipes = self.CozinhaPetDB.Recipes

    def __del__(self):
        self.client.close

    def getSimilaritySearchableRegex(self, term):
        # remove acentos e caracteres estranhos
        searchable = unidecode.unidecode(term).upper()
        # gera a expressão regular que tenha o termo
        # em qualquer posição da string
        regx = re.compile(r'(?i){}'.format(searchable))

        return regx

    def getExactSearchableRegex(self, term):
        # Remove caracteres estranhos
        searchable = unidecode.unidecode(term).upper()
        # Gera a expressão regular que inicie com o termo (^)
        # e finalize com o termo ($) - ou seja, só contém o termo
        # ignorandomaiusculas e minusculas
        regx = re.compile(r'(?i)^{}$'.format(searchable))

        return regx
