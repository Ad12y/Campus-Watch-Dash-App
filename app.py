import dash
from dash.dependencies import Input, Output
from layouts import create_home_layout
from callbacks import update_figures, display_data_summary
import dash_bootstrap_components as dbc
import pandas as pd

# Define your Mapbox access token
mapbox_access_token = 'pk.eyJ1Ijoic2luZ2hhbDEyIiwiYSI6ImNrYjdzMGhzYzAyN3AyeG85bnQ0bWZoZjYifQ.qpQ8v1B5wLlXZLIsRLb78Q'

# Sample DataFrame
df = pd.read_csv("data/df_pdf_latlong.csv")

# Convert the 'Report Date' column to datetime format
df['Report Date'] = pd.to_datetime(df['Report Date'], format='%d/%m/%y %H%MHrs', errors='coerce')

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], title="A Data-Driven Approach to Crime and Fire Safety at Rutgers University, New Brunswick")

# Define the layout
app.layout = create_home_layout(df)

# Define callbacks
@app.callback(
    [Output('density-map', 'figure'),
     Output('top-crimes-chart', 'figure')],
    [Input('crime-type-dropdown', 'value'),
     Input('status-radio', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_figures_callback(crime_type, status, start_date, end_date):
    return update_figures(df, crime_type, status, start_date, end_date, mapbox_access_token)

@app.callback(
    Output('area-wise-crimes', 'children'),
    [Input('crime-type-dropdown', 'value'),
     Input('status-radio', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def display_data_summary_callback(crime_type, status, start_date, end_date):
    return display_data_summary(df, crime_type, status, start_date, end_date)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)