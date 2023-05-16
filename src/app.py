from flask import Flask, config, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from flask_bootstrap import Bootstrap5
from backend.queries import query_firely_server

app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/callback', methods=['POST', 'GET'])
def cb():
    data = request.get_json()
    graph_type = data["graph_type"]
    resource = data["resource"]
    data_element_x = data["data_element_x"]
    data_element_y = data["data_element_y"]
    return gm(resource, graph_type, data_element_x, data_element_y)
   
@app.route('/')
def index():
    # return render_template('index.html',  graphJSON=gm(data_path, resource, graph_type, data_element_x, data_element_y))
    return render_template('index.html')

def gm(resource, graph_type, data_element_x, data_element_y):
    # read data and define dataframes
    if data_element_x != '':
        data = query_firely_server(resource=resource, x=data_element_x, date_filter=False, date_from=None, date_to=None, y=data_element_y)
    else:
        data = query_firely_server(resource=resource, x=data_element_x, date_filter=False, date_from=None, date_to=None, y=None)
    x_var = data[data_element_x]
    y_var = data[data_element_y]
    print(x_var)

    # Define the chart
    if graph_type == 'Line graph':
        fig = go.Figure(data=[go.Scatter(x=x_var, y=y_var, mode='lines')])
        fig.update_layout(title='Line Chart', xaxis_title=data_element_x, yaxis_title=data_element_y)
    elif graph_type == 'Bar graph':
        df = data.groupby(data_element_x)[data_element_y].sum().reset_index()
        fig = go.Figure(data=[go.Bar(x=df[data_element_x], y=df[data_element_y])])
        fig.update_layout(title='Bar graph', xaxis_title=data_element_x, yaxis_title=data_element_y)
    elif graph_type == 'Pie chart':
        df = data.groupby(data_element_x).size().rename('Value').reset_index()
        fig = go.Figure(data=[go.Pie(labels=df[data_element_x], values=df['Value'])])
        fig.update_layout(title='Pie chart', xaxis_title=data_element_x, yaxis_title=data_element_y)
    elif graph_type == 'scatterplot':
        fig = go.Figure(data=[go.Scatter(x=x_var, y=y_var, mode='markers')])
        fig.update_layout(title='Scatterplot', xaxis_title=data_element_x, yaxis_title=data_element_y)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    print(fig.data[0])
    
    return graphJSON