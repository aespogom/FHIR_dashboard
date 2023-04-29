from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('allergies.csv') 

temp = df.groupby(["START", "DESCRIPTION"]).size()
temp1 = temp.rename('amount affected').reset_index()

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Allergies', style={'textAlign':'center'}),
    dcc.Dropdown(df.DESCRIPTION.unique(), 'Latex (substance)', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = temp1[temp1.DESCRIPTION==value]
    return px.line(dff, x='START', y='amount affected')


if __name__ == '__main__':
    app.run_server(debug=True)
