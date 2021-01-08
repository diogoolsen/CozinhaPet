
ingredient = {
    'name': 'abobrinha',
    'type': 'vegetal',      # meat, vegetable, supplement
    'unity': 'g',           # g, ml, undefined (if supplement)
    'factorsLog': [factors_list],
    'costLog': [cost_list],
    'stockLog': False       # True\False
    'stock': [stock_list]
}

factors_list = {
    'date': date.today()
    'cookingFactor': 1.,
    'safetyMargin': 1.,
    'actualFactor': 1.
}

cost_list = {
    'date': date.today(),
    'price': 31.4,
    'amount': 1000.,
    'costPer1Unity': 0.00314,
    'costPer1K': 31.4
}

stock_list = {
    'date': date.today(),
    'amount': 1000.,
}
