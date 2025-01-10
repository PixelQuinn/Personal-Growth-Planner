import requests
import pandas as pd

# Set up API key
api_key = "YOUR_API_KEY_HERE"
base_url = "https://api.spoonacular.com/recipes/complexSearch"

# Take user input
print("Welcome to the Recipe Fetcher!")
meal_type = input("Enter the meal type (e.g. breakfast, lunch, dinner): ").strip().lower()
calorie_limit = int(input("Enter the maximum calories per recipe: "))
recipe_count = int(input("How many recipes would you like to fetch?: "))

# Define query params
params = {
    "apiKey": api_key,
    "number": recipe_count, # <-- Number of recipes to fetch
    "type": meal_type, # <-- Filter by meal type
    "maxCalories": calorie_limit # <-- The limit on calories per meal
}