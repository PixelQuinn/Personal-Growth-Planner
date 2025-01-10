import requests
import pandas as pd

# Set up API key
api_key = "YOUR_API_KEY_HERE"
base_url = "https://api.spoonacular.com/recipes/complexSearch"

# Define query params
params = {
    "apiKey": api_key,
    "number": 10, # <-- Number of recipes to fetch
    "type": "main course", # <-- Filter by meal type
    "maxCalories": 600
}