import requests
import json

api_key = 'ec5c7ec2c3b8ae12a77ad94680300b66'
form_id = '241066292962056'
url = f'https://api.jotform.com/form/{form_id}/submissions?apiKey={api_key}'

response = requests.get(url)
data = response.json()

# Pretty print the JSON data to understand its structure
print(json.dumps(data, indent=4))
