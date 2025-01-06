import json
import re
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


df = pd.read_excel('./data/IIITB-Menu.xlsx')

menu_title = df.columns[0]

def extract_dates(text):
    # Extract dates in DD/MM/YYYY format
    pattern = r'(\d{2}/\d{2}/\d{4})'
    dates = re.findall(pattern, text)
    return dates


def get_dates_for_weekday(start_date_str, end_date_str, weekday):
    def add_suffix(day):
        try:
            day = int(day)
        except ValueError:
            pass

        if day in [1, 21, 31]:
            return f"{day}st"
        elif day in [2, 22]:
            return f"{day}nd"
        elif day in [3, 23]:
            return f"{day}rd"
        else:
            return f"{day}th"

    # Dictionary to map weekday names to numbers (0 = Monday, 6 = Sunday)
    weekdays = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }
    
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
    end_date = datetime.strptime(end_date_str, '%d/%m/%Y')
    
    # Get the weekday number
    target_weekday = weekdays[weekday.lower()]
    
    # Find all dates of the specified weekday
    dates = []
    current_date = start_date
    
    while current_date <= end_date:
        if current_date.weekday() == target_weekday:
            # dates.append(current_date.strftime('%d/%m/%Y'))
            dates.append(current_date.strftime('%B ') + add_suffix(current_date.day) + current_date.strftime(' %Y'))
        current_date += timedelta(days=1)
    
    return dates


date_start, date_end = extract_dates(menu_title)



def capitalize_if_string(i):
    if isinstance(i, str):
        return i.capitalize()
    return i

# Set the days of the week as column names
df.columns = [capitalize_if_string(i) for i in df.iloc[0]]
df = df.drop(df.index[0])


# Make empty cells empty
df = df.replace('\xa0', np.nan)
df = df.replace(np.nan, '')

# Title-ify names
df = df.applymap(lambda x: str(x).strip())
df = df.applymap(lambda x: str(x).title())


days = ['Sunday', 'Monday', 'Tuesday',
        'Wednesday', 'Thursday', 'Friday', 'Saturday']
meals = ['Breakfast', 'Lunch', 'Snacks', 'Dinner']

data = {}

def process_meal_data(series):
    """
    Process a pandas series containing meal data into a structured dictionary format.
    
    Args:
        series: pandas.Series containing meal items with meal categories
        
    Returns:
        list: List of dictionaries containing meal categories and their items
    """
    # Initialize variables
    result = []
    current_category = None
    current_items = []
    
    # Define meal categories
    meal_categories = {'Breakfast', 'Lunch', 'Snacks', 'Dinner'}
    
    # Process each row in the series
    for item in series:
        # Skip empty or whitespace-only strings
        if not isinstance(item, str) or not item.strip():
            continue
            
        # Clean the item string
        item = item.strip()
        
        # Check if this is a meal category
        if item in meal_categories:
            # Save previous category if exists
            if current_category:
                result.append({
                    'title': current_category,
                    'items': current_items
                })
            # Start new category
            current_category = item
            current_items = []
        # If not a category and we have a current category, add to items
        elif current_category and item:
            current_items.append(item)
    
    # Add the last category
    if current_category and current_items:
        result.append({
            'title': current_category,
            'items': current_items
        })
    
    return result


for day in days:
    data[day] = {
        'dates': get_dates_for_weekday(date_start, date_end, day), 
        'catalog': process_meal_data(df[day])
    }



print(data)

with open('./data/menu.json', 'w') as jsonfile:
    json.dump(data, jsonfile)