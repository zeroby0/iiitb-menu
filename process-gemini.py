import json
import os
import pandas as pd
import numpy as np
from python_calamine.pandas import pandas_monkeypatch
from google import genai

pandas_monkeypatch()
df = pd.read_excel("./data/IIITB-Menu.xlsx", engine="calamine")

days = ['Sunday', 'Monday', 'Tuesday',
        'Wednesday', 'Thursday', 'Friday', 'Saturday']
meals = ['Breakfast', 'Lunch', 'Snacks', 'Dinner']

def try_to_make_df_reasonable(df):
    def capitalize_if_string(i):
        if isinstance(i, str):
            return i.capitalize()
        return i

    df.columns = [capitalize_if_string(i) for i in df.columns]

    # Make empty cells NaN
    df = df.replace("\xa0", np.nan)

    # Why do they want backslashes in the menu?
    df = df.replace("\\", "/")

    # Make empty cells empty
    df = df.replace(np.nan, "")

    # # Title-ify names
    df = df.map(lambda x: str(x).strip())
    df = df.map(lambda x: str(x).title())

    # Sort days in preferred order.
    df = df[days]

    return df


try:
    df = try_to_make_df_reasonable(df)
except Exception:
    # The foodcomm has messed up the format YET AGAIN for no good reason
    # Throw without any pre-processing at the LLM
    pass



print(df)

llm = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response_schema = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "dates": {"type": "ARRAY", "items": {"type": "STRING"}},
            "day_of_the_week": {
                "type": "STRING",
                "enum": days,
            },
            "catalog": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "title": {"type": "STRING", "enum": meals},
                        "items": {"type": "ARRAY", "items": {"type": "STRING"}},
                    },
                },
            },
        },
        "required": ["dates", "catalog"],
    },
}

config = {
    "response_mime_type": "application/json",
    "response_schema": response_schema,
}

response = llm.models.generate_content(
    model="gemini-2.5-flash",
    contents=["Convert the following table into JSON. Format dates like July 21st, ignoring Year and Time.\n", df.to_string()],
    config=config,
)

print(response.parsed)

menu_json = {}
for day in days:
    for i in response.parsed:
        # Tryna ensure days of the week are in the right order
        if i['day_of_the_week'] == day:
            del(i['day_of_the_week'])
            menu_json[day] = i


print(menu_json)

with open('./data/menu.json', 'w') as jsonfile:
    json.dump(menu_json, jsonfile)