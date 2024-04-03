import json

import pandas as pd
import numpy as np


df = pd.read_excel('./data/IIITB-Menu.xlsx')

# df = df.drop('Unnamed: 1', axis=1)
df = df.drop(df.columns[1], axis=1) # Drop the meal subtype column

# Set the first row as names of columns
df.columns = df.iloc[0]
df = df.drop(df.index[0])


def human_readable_time(date):
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
    
    dt = pd.to_datetime(date).dt

    return dt.strftime('%B ') + dt.day.apply(add_suffix) + dt.strftime(' %Y')


def capitalize_if_string(i):
    if isinstance(i, str):
        return i.capitalize()
    return i


# Get names of columns from Row 1
# Sometimes they somehow add NaNs into the excel file,
# and so I'd like to ensure it's a string before calling
# capitalize on it.
# df.columns = [capitalize_if_string(i) for i in df.iloc[0]]
df.columns = [capitalize_if_string(i) for i in df.columns] # - TEMP FIX 17 JULY

# Remove name row - TEMP FIX 17 JULY
# df = df.drop(index=[0])

# Make empty cells NaN
df = df.replace('\xa0', np.nan)

# Make first col Meals
df = df.rename(columns={df.columns[0]: 'Meal'})
df['Meal'] = df['Meal'].ffill()

# Make empty cells empty
df = df.replace(np.nan, '')

# Title-ify names
df = df.applymap(lambda x: str(x).strip())
df = df.applymap(lambda x: str(x).title())

# Convert dates to human readable format
df.iloc[0] = human_readable_time(df.iloc[0])
df.iloc[1] = human_readable_time(df.iloc[1])


days = ['Sunday', 'Monday', 'Tuesday',
        'Wednesday', 'Thursday', 'Friday', 'Saturday']
meals = ['Breakfast', 'Lunch', 'Snacks', 'Dinner']

data = {}


# Replace Daal Pakwaan with Daal Bakvaas
df[df['Meal'] == 'Snacks'] = df[df['Meal'] == 'Snacks'].apply(
    lambda x: x.str.replace(r'Pakwaan', 'Bakvaas', case=False, regex=True))
df[df['Meal'] == 'Snacks'] = df[df['Meal'] == 'Snacks'].apply(
    lambda x: x.str.replace(r'Pakwan', 'Bakvaas', case=False, regex=True))


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
