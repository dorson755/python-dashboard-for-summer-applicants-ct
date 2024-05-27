import requests
import json

api_key = 'ec5c7ec2c3b8ae12a77ad94680300b66'
form_id = '241066292962056'
url = f'https://api.jotform.com/form/{form_id}/submissions?apiKey={api_key}'

response = requests.get(url)
data = response.json()

# Save the JSON data to a file
with open('jotform_data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("JSON data saved to jotform_data.json")
