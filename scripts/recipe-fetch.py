import requests
import pandas as pd

# Set up API key
api_key = "YOUR_API_KEY_HERE"
base_url = "https://api.spoonacular.com/recipes/complexSearch"

# Take user input
print("Welcome to the Recipe Fetcher!")
meal_type = input("Enter the meal type (e.g. breakfast, lunch, dinner): ").strip().lower()
recipe_count = int(input("How many recipes would you like to fetch?: "))

# Define query params
params = {
    "apiKey": api_key,
    "number": recipe_count, # <-- Number of recipes to fetch
    "type": meal_type, # <-- Filter by meal type
}

# API request
response = requests.get(base_url, params=params)
data = response.json()

# Extract relevant info
recipes = []
for recipe in data.get("results", []):
    recipes.append({
        "Recipe Name": recipe.get("title"),
        "Meal Type": meal_type.capitalize(), 
        "Image URL": recipe.get("image"),
        "Recipe URL": f"https://spoonacular.com/recipes/{recipe.get('id')}",
    })

# Save recipes to Excel
df = pd.DataFrame(recipes)
output_file = "MealPrepTracker.xlsx"

try:
    # Load existing Excel file and update the "Recipes" sheet
    with pd.ExcelWriter(output_file, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name="Recipes", index=False)
    print(f"Recipes successfully added to {output_file}.")
except FileNotFoundError:
    # If the file doesn't exist, create a new one
    df.to_excel(output_file, sheet_name="Recipes", index=False)
    print(f"New file {output_file} created with 'Recipes' sheet.")