import os
from flask import Flask, render_template
import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Dash
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')

dash_app.layout = html.Div([
    dcc.Interval(id='interval-component', interval=60000, n_intervals=0),  # Update every minute
    dash_table.DataTable(id='live-update-table')
])

# Callback to update the table
@dash_app.callback(Output('live-update-table', 'data'),
                   Input('interval-component', 'n_intervals'))
def update_table_live(n):
    api_key = os.getenv('JOTFORM_API_KEY')
    form_id = os.getenv('JOTFORM_FORM_ID')
    url = f'https://api.jotform.com/form/{form_id}/submissions?apiKey={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        submissions = data['content']

        # Extract data based on field IDs
        table_data = [
            {
                'First Name': sub['answers']['9']['answer'] if '9' in sub['answers'] else '',
                'Last Name': sub['answers']['8']['answer'] if '8' in sub['answers'] else '',
                'Emergency Contact': sub['answers']['34']['answer'] if '34' in sub['answers'] else '',
                'Telephone': sub['answers']['35']['answer']['full'] if '35' in sub['answers'] else '',
                'School': sub['answers']['37']['answer'] if '37' in sub['answers'] else '',
                'Grade': sub['answers']['38']['answer'] if '38' in sub['answers'] else '',
                'Student Email': sub['answers']['13']['answer'] if '13' in sub['answers'] else '',
                'Age': sub['answers']['16']['answer'] if '16' in sub['answers'] else '',
                'Date of Birth': sub['answers']['15']['prettyFormat'] if '15' in sub['answers'] else '',
            }
            for sub in submissions
        ]

        return table_data

    except requests.exceptions.RequestException as e:
        return []

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
