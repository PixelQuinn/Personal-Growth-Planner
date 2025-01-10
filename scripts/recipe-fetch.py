import requests
import pandas as pd
from openpyxl import load_workbook

# Edamam API credentials
app_id = "YOUR_APP_ID"  # Replace with your Edamam App ID
app_key = "YOUR_APP_KEY"  # Replace with your Edamam App Key
user_id = "YOUR_USER_ID"  # Replace with your Edamam Account User ID
base_url = "https://api.edamam.com/search"

# Function to fetch recipes
def fetch_recipes(meal_type, max_calories, num_recipes):
    recipes = []
    params = {
        "q": meal_type,
        "app_id": app_id,
        "app_key": app_key,
        "calories": f"0-{max_calories}",
        "to": num_recipes  # Number of recipes to fetch
    }
    headers = {
        "Edamam-Account-User": user_id
    }
    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching recipes: {response.status_code}, {response.text}")
        return recipes

    data = response.json()
    for recipe_entry in data.get("hits", []):
        recipe_data = recipe_entry.get("recipe", {})
        recipes.append({
            "Meal Type": meal_type.capitalize(),
            "Recipe Name": recipe_data.get("label", "N/A"),
            "Calories Per Serving": round(recipe_data.get("calories", 0) / recipe_data.get("yield", 1)),
            "Servings": recipe_data.get("yield", "N/A"),
            "Ingredients": ", ".join(recipe_data.get("ingredientLines", [])),
            "Instructions": recipe_data.get("url", "N/A")
        })
    return recipes

# User input
print("Welcome to the Recipe Fetcher!")
meal_type = input("Enter the meal type (e.g., breakfast, lunch, dinner, snack): ").strip().lower()
max_calories = input(f"Enter the maximum calories for {meal_type}: ").strip()
num_recipes = int(input("How many recipes would you like to fetch?: "))

# Fetch recipes
new_recipes = fetch_recipes(meal_type, max_calories, num_recipes)

# Load existing data from Excel
output_file = "MealPrepTracker.xlsx"
try:
    existing_df = pd.read_excel(output_file, sheet_name="Recipes")
except FileNotFoundError:
    existing_df = pd.DataFrame()  # No existing file, start with empty DataFrame

# Combine new recipes with existing data
df_new_recipes = pd.DataFrame(new_recipes)
if not existing_df.empty:
    combined_df = pd.concat([existing_df, df_new_recipes]).drop_duplicates(subset=["Recipe Name"])
else:
    combined_df = df_new_recipes

# Save updated data back to Excel
try:
    with pd.ExcelWriter(output_file, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        combined_df.to_excel(writer, sheet_name="Recipes", index=False)
    print(f"Successfully added {len(new_recipes)} new recipes to {output_file}.")
except Exception as e:
    print(f"Error saving recipes to Excel: {e}")
