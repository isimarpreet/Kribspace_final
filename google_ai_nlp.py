import requests
import json

API_KEY = 'AIzaSyBlnb_LaAkf7-hs_Fd-7-5IiGcs4yYSmtI'  # Replace with your actual API key

def process_query(natural_query):
    url = f'https://language.googleapis.com/v1/documents:analyzeSyntax?key={API_KEY}'
   
    document = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': natural_query
        },
        'encodingType': 'UTF8'
    }

    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(document))

    if response.status_code == 200:
        response_data = response.json()
        return generate_sql_query(response_data)
    else:
        raise Exception(f"Error calling Google API: {response.status_code} {response.text}")

def generate_sql_query(nlp_data):
    base_query = "SELECT * FROM properties WHERE"
    conditions = []
    budget = None
    year_built = None

    for token in nlp_data['tokens']:
        word = token['text']['content']
        part_of_speech = token['partOfSpeech']['tag']

        if part_of_speech == 'NOUN':
            if word.lower() in ['house', 'apartment', 'condo', 'townhouse']:
                conditions.append(f"property_type = '{word.capitalize()}'")
            elif word.lower() in ['new', 'good', 'fair', 'needs renovation']:
                conditions.append(f"property_condition = '{word.capitalize()}'")
            elif word.lower() in ['pool', 'garage', 'garden', 'gym']:
                conditions.append(f"amenities LIKE '%{word}%'")
            else:
                conditions.append(f"location LIKE '%{word}%'")
        elif part_of_speech == 'NUM':
            # Contextual number handling (e.g., budget and year built)
            # This is a simplistic example; real-world cases require more sophisticated handling
            if 'budget' in conditions:
                budget = word
            elif 'year' in conditions:
                year_built = word
        elif part_of_speech == 'ADJ':
            if word.lower() in ['new', 'good', 'fair', 'needs renovation']:
                conditions.append(f"property_condition = '{word.capitalize()}'")

    if budget:
        conditions.append(f"budget <= {budget}")
    if year_built:
        conditions.append(f"year_built >= {year_built}")

    if conditions:
        sql_query = f"{base_query} {' AND '.join(conditions)}"
    else:
        sql_query = "SELECT * FROM properties"

    return sql_query
