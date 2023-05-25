from datetime import datetime, timezone
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
    date_format = '%Y-%m-%d %H:%M:%S'
    start_date = None
    end_date = None
    if data["start_date"]:
        d = datetime.fromisoformat(data["start_date"][:-1]).astimezone(timezone.utc).strftime(date_format)
        start_date =  datetime.strptime(d, date_format)
    if data["end_date"]:
        d = datetime.fromisoformat(data["end_date"][:-1]).astimezone(timezone.utc).strftime(date_format)
        end_date =  datetime.strptime(d, date_format)
    additional_filter_resource = data["filters"] if "filters" in data else None
    return gm(resource, graph_type, data_element_x, data_element_y, start_date, end_date, additional_filter_resource)

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

def gm(resource, graph_type, data_element_x, data_element_y, start_date, end_date, advance_filter):
    # read data and define dataframes
    if data_element_y != '' or data_element_y != 'amountvalue':
        data = query_firely_server(resource=resource, x=data_element_x, y=data_element_y, date_from=start_date, date_to=end_date, filters=advance_filter)
    else:
        data = query_firely_server(resource=resource, x=data_element_x, date_from=start_date, date_to=end_date, filters=advance_filter)
    
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