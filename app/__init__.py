from flask import Flask, config, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from flask_bootstrap import Bootstrap5

# configs and received from frontend
data_path = 'app\\static\\data\\' # this will probably be difference once we receive data from the database
# graph_type = 'barchart'
# resource = 'patients'
# data_element_x = 'GENDER'
# data_element_y = 'HEALTHCARE_EXPENSES'

app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/callback', methods=['POST', 'GET'])
def cb():
    data = request.get_json()
    graph_type = data["graph_type"]
    resource = data["resource"]
    data_element_x = data["data_element_x"]
    data_element_y = data["data_element_y"]
    return gm(data_path, resource, graph_type, data_element_x, data_element_y)
   
@app.route('/')
def index():
    # return render_template('index.html',  graphJSON=gm(data_path, resource, graph_type, data_element_x, data_element_y))
    return render_template('index.html')

def gm(data_path, resource, graph_type, data_element_x, data_element_y):
    # read data and define dataframes
    data = pd.read_csv(data_path + resource + '.csv')
    x_var = data[data_element_x]
    if data_element_y != '':
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