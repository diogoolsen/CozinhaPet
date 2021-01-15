
import datetime

factors_list = {
    'date': datetime.datetime.now(),
    'cookingFactor': 1.,
    'safetyMargin': 1.,
    'actualFactor': 1.
}

cost_list = {
    'date': datetime.datetime.now(),
    'price': 31.4,
    'amount': 1000.,
    'costPer1Unity': 0.00314,
    'costPer1K': 31.4
}

stock_list = {
    'date': datetime.datetime.now(),
    'amount': 1000.,
}

ingredient = {
    'name': 'abobrinha',
    'searchable': 'ABOBRINHA',
    'type': 'vegetal',      # meat, vegetable, supplement
    'unity': 'g',           # g, ml, undefined (if supplement)
    'costLog': [cost_list],
    'establishedCostPer1K': 3.75,
    'factorsLog': [factors_list]
}

ingredientRecipe = {
    'name': 'abobrinha',
    'searchable': 'ABOBRINHA',
    'type': 'vegetal',      # meat, vegetable, supplement
    'unity': 'g',           # g, ml, undefined (if supplement)
    'currentActualCookingFactor': 0.89,
    'establishedCostPer1K': 3.75,
    'dailyAmount': 0.037
}

recipeInfo = {
    'petName': 'Ozzy',
    'petSearchable': 'OZZY',
    'tutorName': 'Diogo Olsen',
    'tutorSearchable': 'DIOGO OLSEN',
    'nutricionistName': 'Kássia Menolli',
    'nutricionistSeachable': 'KASSIA MENOLLI',
    'recipeName': 'Frango com Batata',
    'recipeNameSearchable': 'FRANGO COM BATATA',
    # 'registrationNumber': '1',
    'date': datetime.datetime.now(),
    'ingredientsRecipeList': []
}

# Deve ter a função de atualizar os fatores e custos de todos os ingredientes
# Isso deve/pode ser feito gerando uma nova receita e mantendo a velha no BD
# Atualizando a receita é possível gerar um novo orçamento, lista de compras e
#   ficha de produção

# Lote Dias X Embalagens por dia
