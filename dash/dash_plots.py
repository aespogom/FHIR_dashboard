from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# configs and received from frontend
data_path = '/home/dilaratank/Desktop/FHIRdevdays/synthea/synthea_output/csv/'

graph_type = 'linechart'
dataframe = 'patients'
data_element_x = 'INCOME'
data_element_y = 'HEALTHCARE_EXPENSES'


# Define the app
app = Dash(__name__)

# Read the data from the CSV file
data = pd.read_csv(data_path + dataframe + '.csv')

# Define the x and y variables as DataFrames
x_var = data[data_element_x]
if graph_type != 'piechart':
    y_var = data[data_element_y]

# Define the layout of the app
app.layout = html.Div([
    html.Button(id='update-button', n_clicks=0, children='Update'),
    dcc.Graph(id='chart')
])

# Define the line chart
if graph_type == 'linechart':
    fig = go.Figure(data=[go.Scatter(x=x_var, y=y_var, mode='markers')])
    fig.update_layout(title='Line Chart', xaxis_title=data_element_x, yaxis_title=data_element_y)
elif graph_type == 'barchart':
    df = data.groupby(data_element_x)[data_element_y].sum().reset_index()
    fig = go.Figure(data=[go.Bar(x=df[data_element_x], y=df[data_element_y])])
    fig.update_layout(title='Bar Chart', xaxis_title=data_element_x, yaxis_title=data_element_y)
elif graph_type == 'piechart':
    df = data.groupby(data_element_x).size().rename('Value').reset_index()
    fig = go.Figure(data=[go.Pie(labels=df[data_element_x], values=df['Value'])])
    fig.update_layout(title='Pie Chart', xaxis_title=data_element_x, yaxis_title=data_element_y)

# Define the callback function to update the chart
@app.callback(
    Output('chart', 'figure'),
    [Input('update-button', 'n_clicks')]
)
def update_chart(n_clicks):
    return fig

# Start the app
if __name__ == '__main__':
    app.run_server(debug=True)
