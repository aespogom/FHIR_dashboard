from flask import Flask, config, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import openai
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
    start_date = data["start_date"] if "start_date" in data else None 
    end_date = data["end_date"] if "end_date" in data else None
    additional_filter_resource = data["additional_filter_resource"] if "additional_filter_resource" in data else None
    additional_filter_variable = data["additional_filter_variable"] if "additional_filter_variable" in data else None
    return gm(resource, graph_type, data_element_x, data_element_y)

@app.route('/generate', methods=['POST'])
def ai():
    data = request.get_json()
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=data["prompt"],
        temperature=0.6, 
        max_tokens=1000
    )
    return response


@app.route('/')
def index():
    return render_template('index.html')

def gm(resource, graph_type, data_element_x, data_element_y):
    # read data and define dataframes
    if data_element_y != '' or data_element_y != 'amountvalue':
        data = query_firely_server(resource=resource, x=data_element_x, y=data_element_y, date_filter=False)
    else:
        data = query_firely_server(resource=resource, x=data_element_x, date_filter=False)
    
    if data_element_y == 'amountvalue':
        df = data.groupby(data_element_x)[data_element_y].sum().reset_index()
        df = data.groupby(data_element_x).size().rename('amountvalue').reset_index()
        data = df

    x_var = data[data_element_x]
    y_var = data[data_element_y]

    # Define the chart
    title = graph_type + " plotting " + data_element_x + (" and " + data_element_y if data_element_y != "" else "")

    if graph_type == 'Line graph':
        fig = go.Figure(data=[go.Scatter(x=x_var, y=y_var, mode='lines')])
        fig.update_layout(title=title, xaxis_title=data_element_x, yaxis_title=data_element_y)
    elif graph_type == 'Bar graph':
        df = data.groupby(data_element_x)[data_element_y].sum().reset_index()
        fig = go.Figure(data=[go.Bar(x=df[data_element_x], y=df[data_element_y])])
        fig.update_layout(title=title, xaxis_title=data_element_x, yaxis_title=data_element_y)
    elif graph_type == 'Pie chart':
        df = data.groupby(data_element_x).size().rename('Value').reset_index()
        fig = go.Figure(data=[go.Pie(labels=df[data_element_x], values=df['Value'])])
        fig.update_layout(title=title, xaxis_title=data_element_x, yaxis_title=data_element_y)
    elif graph_type == 'Scatter plot':
        fig = go.Figure(data=[go.Scatter(x=x_var, y=y_var, mode='markers')])
        fig.update_layout(title=title, xaxis_title=data_element_x, yaxis_title=data_element_y)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    print(fig.data[0])
    
    return graphJSON