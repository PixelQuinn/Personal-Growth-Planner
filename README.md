# Meal Prep Tracker

Meal Prep Tracker is a comprehensive Excel-based tool designed to help you efficiently plan your meals, track calories, and maintain an organized recipe database. This project is user-friendly and aims to support personal health and organizational goals.

## Features

- **Meal Plan Calendar**: 
  - Organized by weeks (Week 1 - Week 4).
  - Includes dropdown menus for meal selection.
  - Automatically calculates calories for each meal.

- **Recipes Sheet**:
  - Stores detailed recipe information, including:
    - Meal type (Breakfast, Lunch, Dinner, Snack).
    - Recipe name.
    - Calories per serving.
    - Ingredients.
    - Instructions.

- **Dynamic Dropdowns**:
  - Filters recipes based on meal type for easy selection.

- **Calorie Tracking**:
  - Automatically sums up daily and weekly calorie intake.

## How to Use

1. **Set Up Your Recipes**:
   - Navigate to the **Recipes** sheet.
   - Add new recipes with the following details:
     - Meal type (e.g., Breakfast, Lunch).
     - Recipe name.
     - Calories per serving.
     - Ingredients.
     - Instructions.

2. **Plan Your Meals**:
   - Navigate to the **Meal Plan** sheet.
   - Select meals for each day using the dropdown menus.
   - The sheet will automatically calculate the total calories for each meal and day.

3. **Track Your Progress**:
   - Review calorie totals for each day and week to ensure you meet your goals.

## Script for Automating Recipe Input

This Python script fetches recipes dynamically and updates the **Recipes Sheet** in your Excel file.

### Prerequisites
- Install Python libraries:
  pip install pandas openpyxl requests