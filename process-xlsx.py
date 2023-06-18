import json

import pandas as pd
import numpy as np


df = pd.read_excel('./data/IIITB-Menu.xlsx')

df = df.drop('Unnamed: 1', axis=1)

# Get names of columns from Row 1
df.columns = [i.capitalize() for i in df.iloc[0]]

# Remove name row
df = df.drop(index=[0])

# Make empty cells NaN
df = df.replace('\xa0', np.nan)

# Make first col Meals
df = df.rename(columns={df.columns[0]: 'Meal'})
df['Meal'] = df['Meal'].fillna(method='ffill')

# Make empty cells empty
df = df.replace(np.nan, '')

# Title-ify names
df = df.applymap(lambda x: str(x).strip())
df = df.applymap(lambda x: str(x).title())

# Make datetime rows date string
df.iloc[0] = pd.to_datetime(df.iloc[0]).dt.strftime('%B %dth %Y')
df.iloc[1] = pd.to_datetime(df.iloc[1]).dt.strftime('%B %dth %Y')

days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
meals = ['Breakfast', 'Lunch', 'Snacks', 'Dinner']

data = {}

for day in days:
    data[day] = {
        'dates': [],
        'catalog': []
    }
    
    data[day]['dates'] = list(df[day][0:2])

    for meal in meals:
        s = df[day][df['Meal'] == meal]
        s = s[s != '']
        
        data[day]['catalog'].append({
            'title': meal,
            'items': s.tolist()
        })
        

with open('./data/menu.json', 'w') as jsonfile:
    json.dump(data, jsonfile)