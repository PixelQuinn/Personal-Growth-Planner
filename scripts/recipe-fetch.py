import requests
import pandas as pd

# Set up API key
api_key = "YOUR_API_HERE"
search_url = "https://api.spoonacular.com/recipes/complexSearch"
info_url = "https://api.spoonacular.com/recipes/{id}/information"

# Take user input
print("Welcome to the Recipe Fetcher!")
meal_type = input("Enter the meal type (e.g., breakfast, lunch, dinner): ").strip().lower()
recipe_count = int(input("How many recipes would you like to fetch?: "))
calorie_limit = int(input("What is the amount of calories you'd like to limit yourself to?: "))

# Define query params for recipe search
params = {
    "apiKey": api_key,
    "number": recipe_count,  # Number of recipes to fetch
    "type": meal_type,  # Filter by meal type
    "maxCalories": calorie_limit,  # Limit calories for meals
}

# API request to search for recipes
response = requests.get(search_url, params=params)
data = response.json()

# Extract relevant info
recipes = []
for recipe in data.get("results", []):
    recipe_id = recipe.get("id")  # Get the recipe ID
    title = recipe.get("title")  # Recipe title
    image = recipe.get("image")  # Recipe image URL
    recipe_url = f"https://spoonacular.com/recipes/{recipe_id}"  # Recipe URL

    # API request to fetch detailed recipe info
    info_response = requests.get(info_url.format(id=recipe_id), params={"apiKey": api_key})
    info_data = info_response.json()

    # Extract ingredients
    ingredients = ", ".join(
        [ingredient.get("original", "") for ingredient in info_data.get("extendedIngredients", [])]
    ) if info_data.get("extendedIngredients") else "N/A"

    # Extract calories
    calories_data = info_data.get("nutrition", {}).get("nutrients", [])
    calories = next((item["amount"] for item in calories_data if item.get("name") == "Calories"), "N/A")

    recipes.append({
        "Recipe Name": title,
        "Meal Type": meal_type.capitalize(),
        "Calories": calories,
        "Image URL": image,
        "Recipe URL": recipe_url,
        "Ingredients": ingredients,
    })

# Save recipes to Excel
df = pd.DataFrame(recipes)
output_file = "MealPrepTracker.xlsx"

try:
    # Load existing Excel file and update the "Recipes" sheet
    existing_df = pd.read_excel(output_file, sheet_name="Recipes")
    combined_df = pd.concat([existing_df, df]).drop_duplicates(subset="Recipe Name")
except FileNotFoundError:
    # If the file doesn't exist, create a new one
    combined_df = df

# Save the updated recipes to the "Recipes" sheet
with pd.ExcelWriter(output_file, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    combined_df.to_excel(writer, sheet_name="Recipes", index=False)

print(f"{len(recipes)} recipes successfully added to the 'Recipes' sheet in {output_file}.")
