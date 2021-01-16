

from src.model.recipe import Recipe
from src.data_base.recipes_DB import RecipesDB

recipesDB = RecipesDB()

recipesDB.Recipes.delete_many({})

recipe = Recipe('Bruce', 'Diogo', 'Kássia', 'Bruce - Carne com Batata')
recipesDB.addRecipe(recipe)

recipe = Recipe('Ozzy', 'Marcela', 'Kássia', 'Ozzy - Porco com Abobrinha')
recipesDB.addRecipe(recipe)

recipe = Recipe('Rex', 'Zé', 'Kássia', 'Rex - Peixe com legumes')
recipesDB.addRecipe(recipe)

recipe = Recipe('Rex', 'Zé', 'Kássia', 'Rex - Carne com legumes')
recipesDB.addRecipe(recipe)

recipe = Recipe('Rex', 'Zé', 'Kássia', 'Rex - Porco com arroz')
recipesDB.addRecipe(recipe)
