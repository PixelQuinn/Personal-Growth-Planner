import requests
import pandas as pd

# Set up API key
api_key = "YOUR_API_KEY"
search_url = "https://api.spoonacular.com/recipes/complexSearch"
info_url = "https://api.spoonacular.com/recipes/{id}/information"

# User input for parameters
print("Welcome to the Recipe Fetcher!")
meal_type = input("Enter the meal type (e.g., breakfast, lunch, dinner): ").strip().lower()
recipe_count = int(input("How many recipes would you like to fetch?: "))
calorie_limit = int(input("Enter a calorie limit per recipe: "))

# Define query parameters
params = {
    "apiKey": api_key,
    "number": recipe_count,
    "type": meal_type,
    "maxCalories": calorie_limit,  # Filter recipes by calorie limit
}

# API request to search for recipes
response = requests.get(search_url, params=params)
data = response.json()

# Extract relevant recipe information
recipes = []
for recipe in data.get("results", []):
    recipe_id = recipe.get("id")
    title = recipe.get("title")
    recipe_url = f"https://spoonacular.com/recipes/{recipe_id}"

    # Fetch detailed recipe info
    info_response = requests.get(info_url.format(id=recipe_id), params={"apiKey": api_key})
    info_data = info_response.json()

    # Extract ingredients
    ingredients = ", ".join(
        [ingredient.get("original", "") for ingredient in info_data.get("extendedIngredients", [])]
    ) if info_data.get("extendedIngredients") else "N/A"

    # Append recipe data
    recipes.append({
        "Recipe Name": title,
        "Meal Type": meal_type.capitalize(),
        "Recipe URL": recipe_url,
        "Ingredients": ingredients,
    })

# Convert recipes to a DataFrame
df = pd.DataFrame(recipes)

# Save recipes to Excel
output_file = "MealPrepTracker.xlsx"
try:
    # Load existing file if it exists
    try:
        existing_df = pd.read_excel(output_file, sheet_name="Recipes")
        combined_df = pd.concat([existing_df, df]).drop_duplicates(subset="Recipe Name")
    except FileNotFoundError:
        combined_df = df

    # Write to Excel
    with pd.ExcelWriter(output_file, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        combined_df.to_excel(writer, sheet_name="Recipes", index=False)
    print(f"{len(recipes)} recipes successfully added to the 'Recipes' sheet in {output_file}.")
except Exception as e:
    print(f"Failed to save to Excel. Error: {e}")
