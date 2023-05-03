# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly.graph_objs as go
# import pandas as pd

# data = pd.read_csv('test.csv')

# # Define the app
# app = dash.Dash(__name__)

# # Define the layout of the app
# app.layout = html.Div([
#     # dcc.Input(id='x-var', type='text', placeholder='Enter x variable name'),
#     # dcc.Input(id='y-var', type='text', placeholder='Enter y variable name'),
#     # html.Button(id='submit-button', n_clicks=0, children='Submit'),
#     dcc.Graph(id='line-chart')
# ])

# # Define the callback function to update the chart
# @app.callback(
#     dash.dependencies.Output('line-chart', 'figure'),
#     [dash.dependencies.Input('submit-button', 'n_clicks')],
#     [dash.dependencies.State('x-var', 'value'),
#      dash.dependencies.State('y-var', 'value')]
# )
# def update_line_chart(n_clicks, x_var, y_var):
#     # Load the data and search for x and y variables
    
#     if x_var not in data.columns or y_var not in data.columns:
#         return {}
#     x_data = data[x_var]
#     y_data = data[y_var]
    
#     # Create the line chart
#     fig = go.Figure(data=[go.Scatter(x=x_data, y=y_data, mode='lines')])
#     fig.update_layout(title=f'{y_var} vs. {x_var}', xaxis_title=x_var, yaxis_title=y_var)
#     return fig

# # Start the app
# if __name__ == '__main__':
#     app.run_server(debug=True)

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

# Define the app
app = dash.Dash(__name__)

# Read the data from the CSV file
data = pd.read_csv('patients.csv')

# Define the x and y variables as DataFrames
x_var = data['HEALTHCARE_EXPENSES']
y_var = data['INCOME']

# Define the layout of the app
app.layout = html.Div([
    html.Button(id='update-button', n_clicks=0, children='Update'),
    dcc.Graph(id='line-chart')
])

# Define the line chart
fig = go.Figure(data=[go.Scatter(x=x_var, y=y_var, mode='lines')])
fig.update_layout(title='Line Chart', xaxis_title='X Axis', yaxis_title='Y Axis')

# Define the callback function to update the chart
@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('update-button', 'n_clicks')]
)
def update_chart(n_clicks):
    return fig

# Start the app
if __name__ == '__main__':
    app.run_server(debug=True)
