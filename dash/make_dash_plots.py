from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_dash_plot(data_path, graph_type, dataframe, data_element_x, data_element_y):
    
    # read data and define dataframes
    data = pd.read_csv(data_path + dataframe + '.csv')
    x_var = data[data_element_x]
    if graph_type != 'piechart':
        y_var = data[data_element_y]

    # Define the chart
    if graph_type == 'linechart':
        fig = go.Figure(data=[go.Scatter(x=x_var, y=y_var, mode='lines')])
        fig.update_layout(title='Line Chart', xaxis_title=data_element_x, yaxis_title=data_element_y)
    elif graph_type == 'barchart':
        df = data.groupby(data_element_x)[data_element_y].sum().reset_index()
        fig = go.Figure(data=[go.Bar(x=df[data_element_x], y=df[data_element_y])])
        fig.update_layout(title='Bar Chart', xaxis_title=data_element_x, yaxis_title=data_element_y)
    elif graph_type == 'piechart':
        df = data.groupby(data_element_x).size().rename('Value').reset_index()
        fig = go.Figure(data=[go.Pie(labels=df[data_element_x], values=df['Value'])])
        fig.update_layout(title='Pie Chart', xaxis_title=data_element_x, yaxis_title=data_element_y)
    elif graph_type == 'scatterplot':
        fig = go.Figure(data=[go.Scatter(x=x_var, y=y_var, mode='markers')])
        fig.update_layout(title='Line Chart', xaxis_title=data_element_x, yaxis_title=data_element_y)

    # Initialize the Dash app
    app = Dash(__name__)

    # Define the layout
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    return app

if __name__ == '__main__':
    # configs and received from frontend
    data_path = '/home/dilaratank/Desktop/FHIRdevdays/synthea/synthea_output/csv/' # this will probably be difference once we receive data from the database
    graph_type = 'piechart'
    dataframe = 'patients'
    data_element_x = 'GENDER'
    data_element_y = 'HEALTHCARE_EXPENSES'

    app = create_dash_plot(data_path, graph_type, dataframe, data_element_x, data_element_y) # returns dash object
    # app.run_server(debug=True) # you can run it like this

