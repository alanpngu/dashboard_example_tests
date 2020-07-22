import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from sodapy import Socrata
import requests
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

import dash_table
#from pandas import DataFrame
#testing

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


server = app.server 

colors = {
    'background': '#9f9f9f',
    'text': '#111111'
}


client = Socrata("elumitas.demo.socrata.com", None, username = "alan.nguyen@elumitas.com", password = "Fairmont98!")

df = client.get("ggtg-5evq", query = "select incident, count(incident) group by incident having count(incident) > 0")

pd_df = pd.DataFrame(df)

fig = px.bar(pd_df, x= "incident", y="count_incident", color="incident", barmode="group",
            labels = {'incident': 'Incident Type', 'count_incident': 'Number of Incidents'})

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

df2 = client.get("xfbf-mi2s", query = "select max(airtemperature), min(airtemperature), avg(airtemperature) group by stationname")
pd_df2 = pd.DataFrame(df2)

columnlabels = pd_df2.columns


# crime_df = client.get("nu46-gffg", query = "select offense_type, latitude, longitude")
# pd_crime_df = pd.DataFrame(crime_df)

# crime_fig = px.scatter_mapbox(pd_crime_df, lat = pd_crime_df[1], lon = pd_crime_df[2], hover_name = "offense_type", color_discrete_sequence = ["red"])
# #crime_fig.update_layout(mapbox_style="dark", mapbox_accesstoken= "pk.eyJ1IjoiYWxhbndpbjk4IiwiYSI6ImNrY3d5OGNuaTA0bTgzMHFpamV5NzB6aTAifQ.u1TcuBVkdfy8FVCmzBB3Cw")
# #crime_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# #crime_fig.show()

# ctxt = 'WEAPON'
# actual_query = "select summarized_offense, latitude, longitude like '" + ctxt + "'"
# print(actual_query)
# crime_df = client.get("nu46-gffg", query = actual_query)

crime_df = client.get("nu46-gffg", query = "select summarized_offense, latitude, longitude")
pd_crime = pd.DataFrame(crime_df)
ctype = pd_crime.summarized_offense.unique()



# ctxt = "WEAPON"
# actual_query = "select summarized_offense, latitude, longitude where summarized_offense like '" + ctxt + "'"
# crime_df = client.get("nu46-gffg", query = actual_query)
# pd_crime = pd.DataFrame(crime_df)
# ctype = pd_crime.summarized_offense.unique()
# pd_crime["latitude"] = pd.to_numeric(pd_crime["latitude"])
# pd_crime["longitude"] = pd.to_numeric(pd_crime["longitude"])
# fig3 = px.scatter_mapbox(pd_crime, lat=pd_crime.columns[1], lon=pd_crime.columns[2], hover_name = "summarized_offense", color_discrete_sequence = ["fuchsia"], zoom = 10, height = 800)
# fig3.update_layout(mapbox_style="dark", mapbox_accesstoken="pk.eyJ1IjoiYWxhbndpbjk4IiwiYSI6ImNrY3d5OGNuaTA0bTgzMHFpamV5NzB6aTAifQ.u1TcuBVkdfy8FVCmzBB3Cw")
# fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig3.show()

# print(ctype)
# for x in ctype:
#     print
# pd_crime["latitude"] = pd.to_numeric(pd_crime["latitude"])
# pd_crime["longitude"] = pd.to_numeric(pd_crime["longitude"])


# #fig3 = px.scatter_mapbox(crime_df, lat="latitude", lon="longitude", hover_name = "offense_type", color_discrete_sequence = ["fuchsia"], zoom =  3, height = 300)
# fig3 = px.scatter_mapbox(pd_crime, lat=pd_crime.columns[1], lon=pd_crime.columns[2], hover_name = "summarized_offense", color_discrete_sequence = ["fuchsia"], zoom = 10, height = 800)

# fig3.update_layout(mapbox_style="dark", mapbox_accesstoken="pk.eyJ1IjoiYWxhbndpbjk4IiwiYSI6ImNrY3d5OGNuaTA0bTgzMHFpamV5NzB6aTAifQ.u1TcuBVkdfy8FVCmzBB3Cw")
# fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig3.show()

app.layout = html.Div(children=[
    html.H1(
        children='First Try at Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Incident Counts Graph', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    html.H2("Change the query in the text box to see callbacks in action!"),
    html.Div(["Input: ",
              dcc.Input(id='my-input', value='initial value', type='text')]),
    html.Br(),
    html.Div(id='my-output'),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in columnlabels],
                value='tilted'
            )
        ]),
    ]),

    dcc.Graph(
        id='tst-graph'
    ),

    html.Br(),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crime-opt',
                options=[{'label': i, 'value': i} for i in ctype],
                value='All'
            )
        ]),
    ]),
    dcc.Graph(
        id='crime-map'
    ),

])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    [Input(component_id='my-input', component_property='value')]
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)

@app.callback(
    Output('tst-graph', 'figure'),
    [Input('xaxis-column', 'value')]
)
def update_fig(qtxt):
    if(qtxt == 'max_airtemperature'):
        txt = "max(airtemperature)"
    elif(qtxt =='min_airtemperature'):
        txt = "min(airtemperature)"
    else:
        txt = "avg(airtemperature)"
    querz = "select stationname, " + txt + " group by stationname"
    qdf2 = client.get("xfbf-mi2s", query = querz)
    qpdf2 = pd.DataFrame(qdf2)
    figa = px.bar(qpdf2, x = "stationname", y = qpdf2.columns[1], color = 'stationname', barmode = 'group')
    return figa

@app.callback(
    Output('crime-map', 'figure'),
    [Input('crime-opt','value')]
)
def update_crimemap(ctxt):
    if ctxt == 'All':
        actual_query = "select summarized_offense, latitude, longitude"
    else:
        actual_query = "select summarized_offense, latitude, longitude where summarized_offense like '" + ctxt + "'"
    crime_df = client.get("nu46-gffg", query = actual_query)
    pd_crime = pd.DataFrame(crime_df)
    # ctype = pd_crime.summarized_offense.unique()
    pd_crime["latitude"] = pd.to_numeric(pd_crime["latitude"])
    pd_crime["longitude"] = pd.to_numeric(pd_crime["longitude"])
    fig3 = px.scatter_mapbox(pd_crime, lat=pd_crime.columns[1], lon=pd_crime.columns[2], hover_name = "summarized_offense", color_discrete_sequence = ["fuchsia"], zoom = 10, height = 800)
    fig3.update_layout(mapbox_style="dark", mapbox_accesstoken="pk.eyJ1IjoiYWxhbndpbjk4IiwiYSI6ImNrY3d5OGNuaTA0bTgzMHFpamV5NzB6aTAifQ.u1TcuBVkdfy8FVCmzBB3Cw")
    fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig3

if __name__ == '__main__':
    app.run_server(debug=True)