import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from sodapy import Socrata
import requests

import plotly.express as px
import pandas as pd
#from pandas import DataFrame

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



client = Socrata("elumitas.demo.socrata.com", None, username = "alan.nguyen@elumitas.com", password = "Fairmont98!")

df = client.get("ggtg-5evq", query = "select incident, count(incident) group by incident having count(incident) > 0")

pd_df = pd.DataFrame(df)

#print(pd_df)

fig = px.bar(df, x="incident", y="count_incident", color="incident", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)



#d = dict(itertools.zip_longest(*[iter(df)] * 2, fillvalue=""))





# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# # assume you have a "long-form" data frame
# # see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),

#     html.Div(children='''
#         Dash: A web application framework for Python.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)




#client = Socrata("elumitas.demo.socrata.com", None, username = "alan.nguyen@elumitas.com", password = "Fairmont98!")

#df = client.get("ggtg-5evq", query = "select incident, count(incident) group by incident having count(incident) > 5")

#for row in df:
#    print(row)




#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# server = app.server

# app.layout = html.Div([
#     html.H2('Hello Worldzz'),
#     dcc.Dropdown(
#         id='dropdown',
#         options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
#         value='LA'
#     ),
#     html.Div(id='display-value')
# ])

# @app.callback(dash.dependencies.Output('display-value', 'children'),
#               [dash.dependencies.Input('dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)

# if __name__ == '__main__':
#     app.run_server(debug=True)