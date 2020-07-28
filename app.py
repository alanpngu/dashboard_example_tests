import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from sodapy import Socrata
import requests
from dash.dependencies import Input, Output, State

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

import dash_table
import datetime

import pytz

import json


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

epoch = datetime.datetime.utcfromtimestamp(0)

server = app.server 

colors = {
    'background': '#9f9f9f',
    'text': '#111111'
}


client = Socrata("elumitas.demo.socrata.com", None, username = "alan.nguyen@elumitas.com", password = "Fairmont98!")


df2 = client.get("xfbf-mi2s", query = "select max(airtemperature), min(airtemperature), avg(airtemperature) group by stationname")
pd_df2 = pd.DataFrame(df2)
columnlabels = pd_df2.columns


crime_df = client.get("nu46-gffg", query = "select summarized_offense")
pd_crime = pd.DataFrame(crime_df)
ctype = pd_crime.summarized_offense.unique()






app.layout = html.Div(children=[
    html.H1(
        children='First Try at Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),


    html.Div(
        id ='query-mem',
        style={'display': 'none'}
    ),
    html.Div(
        id = 'resetsave'
    ),
    html.Div(
        id = 'printstuff'
    ),
    html.Br(),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crime-opt',
                options=[{'label': i, 'value': i} for i in ctype],
                value='All Crimes'
            )
        ]),
    ]),

    html.Br(),

    html.Button('Reset', id = 'resetbutton', n_clicks = 0, n_clicks_timestamp = 0),
    html.Br(),
    dcc.Graph(
        id = 'hist-graph'
    ),
    html.Br(),
    dcc.Graph(
        id='crime-map'
    ),

    html.Br(),
    html.Br(),


    dcc.Graph(
        id = 'time-graph'
    ),

])

# @app.callback(
#     Output(component_id='my-output', component_property='children'),
#     [Input(component_id='my-input', component_property='value')]
# )
# def update_output_div(input_value):
#     return 'Output: {}'.format(input_value)

# @app.callback(
#     Output('tst-graph', 'figure'),
#     [Input('xaxis-column', 'value')]
# )
# def update_fig(qtxt):
#     if(qtxt == 'max_airtemperature'):
#         txt = "max(airtemperature)"
#     elif(qtxt =='min_airtemperature'):
#         txt = "min(airtemperature)"
#     else:
#         txt = "avg(airtemperature)"
#     querz = "select stationname, " + txt + " group by stationname"
#     qdf2 = client.get("xfbf-mi2s", query = querz)
#     qpdf2 = pd.DataFrame(qdf2)
#     figa = px.bar(qpdf2, x = "stationname", y = qpdf2.columns[1], color = 'stationname', barmode = 'group')
    
#     return figa

# @app.callback(
#     Output('crime-map', 'figure'),
#     [Input('crime-opt','value')]
# )
# def update_crimemap(ctxt):
    # if ctxt == 'All':
    #     actual_query = "select summarized_offense, latitude, longitude"
    # else:
    #     actual_query = "select summarized_offense, latitude, longitude where summarized_offense like '" + ctxt + "'"
    # crime_df = client.get("nu46-gffg", query = actual_query)
    # pd_crime = pd.DataFrame(crime_df)
    # # ctype = pd_crime.summarized_offense.unique()
    # pd_crime["latitude"] = pd.to_numeric(pd_crime["latitude"])
    # pd_crime["longitude"] = pd.to_numeric(pd_crime["longitude"])
    # fig3 = px.scatter_mapbox(pd_crime, lat=pd_crime.columns[1], lon=pd_crime.columns[2], hover_name = "summarized_offense", color_discrete_sequence = ["fuchsia"], zoom = 10, height = 800)
    # fig3.update_layout(mapbox_style="dark", mapbox_accesstoken="pk.eyJ1IjoiYWxhbndpbjk4IiwiYSI6ImNrY3d5OGNuaTA0bTgzMHFpamV5NzB6aTAifQ.u1TcuBVkdfy8FVCmzBB3Cw")
    # fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # return fig3


# @app.callback(
#     Output('time-graph', 'figure'),
#     #Output('crime-map', 'figure')],
#     [Input('crime-opt','value')]
# )
# def update_crimetime(ctxt):
#     if ctxt == 'All Crimes':
#         actual_query = "select count(summarized_offense), occurred_date_or group by occurred_date_or order by occurred_date_or"   
#     else:
#         actual_query = "select count(summarized_offense), occurred_date_or where summarized_offense like '" + ctxt + "' group by occurred_date_or order by occurred_date_or"
#     filt_date_df = client.get("nu46-gffg", query = actual_query)
#     filt_date_crime = pd.DataFrame(filt_date_df)
#     filt_fig = px.line(filt_date_crime, x='occurred_date_or', y='count_summarized_offense', title= "Incidencts of " + ctxt + " Over Time")
#     filt_fig.update_xaxes(
#         rangeslider=dict(
#             visible = True
#         ),
#         rangeselector=dict(
#             buttons=list([
#                 dict(count=1, label="1m", step="month", stepmode="backward"),
#                 dict(count=6, label="6m", step="month", stepmode="backward"),
#                 dict(count=1, label="YTD", step="year", stepmode="todate"),
#                 dict(count=1, label="1y", step="year", stepmode="backward"),
#                 dict(step="all")
#             ])
#         )
#     )


#     timestamps = filt_fig.layout.xaxis.range
#     print(timestamps)
    
    
#     return filt_fig



# @app.callback(
#     Output('fix', 'children'),
#     [Input('time-graph', 'relayoutData')
# ])
# def display_range(fig_data):
#     t1 = "date"
#     if fig_data is not None and 'xaxis.range' in fig_data:
#         t1 = fig_data['xaxis.range'][0]
#         t2 = fig_data['xaxis.range'][1]
#         t1 = t1[0:10]
#         t2 = t2[0:10]
#         print(t1)
#     print(t1)
#     return t1


# @app.callback(
#     Output('crime-map', 'figure'),
#     [Input('time-graph', 'relayoutData'),
#     Input('crime-opt', 'value'),
#     Input('crime-map', 'selectedData')
#     ])
# def display_range(fig_data, ctxt, sel_data): #pull q2 from a storage, and at the same time, save somethign to that storage? 
# #maybe do a if query doesn't exist and if it does kidna thing
#     if fig_data is not None and 'xaxis.range' in fig_data:
#         t1 = fig_data['xaxis.range'][0]
#         t2 = fig_data['xaxis.range'][1]
#         t1 = t1[0:10]
#         t2 = t2[0:10]
#         print(t1)
#         min_time_clause = " occurred_date_or >= '" + t1 + "' "
#         max_time_clause = " occurred_date_or <= '" + t2 + "' "
#         if (ctxt == 'All Crimes'):
#             q2 = "select summarized_offense, latitude, longitude where" + min_time_clause + "AND" + max_time_clause
#         else:
#             q2 = "select summarized_offense, latitude, longitude where summarized_offense like '" + ctxt + "' AND" + min_time_clause + "AND" + max_time_clause 
#         #print(q2)
#         filt_df_q2 = client.get("nu46-gffg", query = q2)
#         q2_crime = pd.DataFrame(filt_df_q2)
#         if (q2_crime["latitude"] is None): #trying to make it empty when nothing appears
#             q2_crime_fig = px.scatter_mapbox(q2_crime, lat=q2_crime.columns[1], lon=q2_crime.columns[2], hover_name = "summarized_offense", color_discrete_sequence = ["fuchsia"], zoom = 10, height = 800)   
#             q2_crime_fig.update_layout(mapbox_style="dark", mapbox_accesstoken="pk.eyJ1IjoiYWxhbndpbjk4IiwiYSI6ImNrY3d5OGNuaTA0bTgzMHFpamV5NzB6aTAifQ.u1TcuBVkdfy8FVCmzBB3Cw")
#             q2_crime_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#         else: #need to make it so it only updates when person lets go
#             q2_crime["latitude"] = pd.to_numeric(q2_crime["latitude"])
#             q2_crime["longitude"] = pd.to_numeric(q2_crime["longitude"]) 
#             q2_crime_fig = px.scatter_mapbox(q2_crime, lat=q2_crime.columns[1], lon=q2_crime.columns[2], hover_name = "summarized_offense", color_discrete_sequence = ["fuchsia"], zoom = 10, height = 800)   
#             q2_crime_fig.update_layout(mapbox_style="dark", mapbox_accesstoken="pk.eyJ1IjoiYWxhbndpbjk4IiwiYSI6ImNrY3d5OGNuaTA0bTgzMHFpamV5NzB6aTAifQ.u1TcuBVkdfy8FVCmzBB3Cw")
#             q2_crime_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#         if(sel_data):
#         # if (sel_data is None):
#         #     return q2_crime_fig
#         # else:
#             txt = sel_data['lassoPoints']['mapbox']
#             lasso_q = "within_polygon(new_location, 'MULTIPOLYGON(((" 
#             temp_zero = ""
#             for i in range(len(txt)):
#                 if (i == 0):
#                     temp_zero = str(txt[i][0]) + " " + str(txt[i][1])
#                     temp_str = temp_zero
#                 else:
#                     temp_str = "," + str(txt[i][0]) + " " + str(txt[i][1])
#                 lasso_q += temp_str
#             lasso_q = lasso_q + ", " + temp_zero + ")))')"
#             print("new_lasso")
#             print(lasso_q)
#             combo_q = q2 + " AND " + lasso_q
#             print(combo_q)
#             crime_combo = client.get("nu46-gffg", query = combo_q)
#             combo_df = pd.DataFrame(crime_combo)
#             combo_df["latitude"] = pd.to_numeric(combo_df["latitude"])
#             combo_df["longitude"] = pd.to_numeric(combo_df["longitude"]) 
#             combo_fig = px.scatter_mapbox(q2_crime, lat=q2_crime.columns[1], lon=q2_crime.columns[2], hover_name = "summarized_offense", color_discrete_sequence = ["fuchsia"], zoom = 10, height = 800)   
#             combo_fig.update_layout(mapbox_style="dark", mapbox_accesstoken="pk.eyJ1IjoiYWxhbndpbjk4IiwiYSI6ImNrY3d5OGNuaTA0bTgzMHFpamV5NzB6aTAifQ.u1TcuBVkdfy8FVCmzBB3Cw")
#             combo_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#             print("did we get here")
#             return combo_fig
#         else:
#             return q2_crime_fig
#             #initialtxt[1] = lasso_q       
#         #return q2_crime_fig
#     else: 
#         return dash.no_update

# #ORIGINAL END





# @app.callback(Output('display','children'),[Input('crime-map','selectedData')])
# def selectData(selectData):
#     return str('Selecting points produces a nested dictionary: {}'.format(selectData))


# @app.callback(Output('filt','children'),[Input('crime-map','selectedData')])
# def selectData3(selectData):

#     txt = selectData['lassoPoints']['mapbox']
#     stringa = "within_polygon(new_location, 'MULTIPOLYGON((("
#     for i in range(len(txt)):
#         if (i == 0):
# #            temp_str = str(txt[i][0]) + " " + str(txt[i][1])
#             temp_zero = str(txt[i][0]) + " " + str(txt[i][1])
#             temp_str = temp_zero
#         else:
#             temp_str = "," + str(txt[i][0]) + " " + str(txt[i][1])
#         stringa += temp_str
#     stringa = stringa + ", " + temp_zero + ")))')"

    #txt = str('{}').format(selectData['lassoPoints']['mapbox'][0])
    #for ()


    # return str('test: {}'.format(selectData['lassoPoints']['mapbox'][0]))
   
    #return str('Selecting points produces a nested dictionary: {}'.format(selectData['lassoPoints']))


# @app.callback(
#     Output('holder1', 'children'),
#     [Input('query-mem', 'children')]
# )


# @app.callback(
#     Output('printstuff','children'),
#     [Input('time-graph', 'relayoutData')]
# )
# def printHehe(relay):
#     # if (relay is not None and 'xaxis.range' in relay):
#     #     t1 = relay['xaxis.range'][0]
#     #     t2 = relay['xaxis.range'][1]
#     #     print(t1)
#     #     print(t2)
#     #     # print(relay['xaxis.rangeslider.range'][0])
#     #     #print(relay['xaxis.rangeslider.range'][1])

#     if (relay is not None and 'xaxis.rangeslider.range' in relay):
#         t3 = relay['xaxis.rangeslider.range'][0]
#         t4 = relay['xaxis.rangeslider.range'][1]
#         print("selector")
#         print(t3)
#         print(t4)
#     return "Printed"

        


@app.callback(
    [Output('query-mem', 'children'),
    Output('resetbutton', 'n_clicks')],
    [Input('crime-opt', 'value'), 
    Input('crime-map','selectedData'),
    Input('time-graph', 'relayoutData'),
    Input('resetsave', 'children')]
)
def savingQuery(val, sel_data, relay_data, reset):
    initialtxt = [''] * 3
    if (val != "All Crimes"):
        crime_type = "summarized_offense like '" + val + "'"
        initialtxt[0] = crime_type
    if (sel_data is not None):
        txt = sel_data['lassoPoints']['mapbox']
        lasso_q = "within_polygon(new_location, 'MULTIPOLYGON((("
        temp_zero = ""
        for i in range(len(txt)):
            if (i == 0):
                temp_zero = str(txt[i][0]) + " " + str(txt[i][1])
                temp_str = temp_zero
            else:
                temp_str = "," + str(txt[i][0]) + " " + str(txt[i][1])
            lasso_q += temp_str
        lasso_q = lasso_q + ", " + temp_zero + ")))')"
        initialtxt[1] = lasso_q
    if (relay_data is not None and 'xaxis.range' in relay_data):
        for i in range(len(relay_data)):
            print(i)
        t1 = relay_data['xaxis.range'][0]
        t2 = relay_data['xaxis.range'][1]
        t1 = t1[0:10]
        t2 = t2[0:10]
        time_clause = " occurred_date_or >= '" + t1 + "' AND" + " occurred_date_or <= '" + t2 + "' "
        initialtxt[2] = time_clause
    if(reset == True):
        initialtxt[0] = ''
        initialtxt[1] = ''
        initialtxt[2] = ''
        return initialtxt,0

    return initialtxt, 0


@app.callback(
    Output('crime-opt', 'value'),
    [Input('resetsave', 'children')]
)
def resetDropdown(reset):
    if (reset == True):
        return "All Crimes"
    else:
        return dash.no_update
    
@app.callback([
    Output('crime-map', 'figure'),
    Output('time-graph', 'figure'),
    Output('hist-graph', 'figure')],
    [Input('query-mem', 'children'),
    Input('crime-opt', 'value')]
)
def pullQuery(qlist, ctxt):
    
    timeline_query = "select count(summarized_offense), occurred_date_or" 
    map_query = "select summarized_offense, latitude, longitude"
    hist_query = "select summarized_offense, count(summarized_offense) " 

    if ((qlist[0] == '' and qlist[1] == '' and qlist[2] == '')):
        timeline_query += " group by occurred_date_or order by occurred_date_or"
        hist_query += " group by summarized_offense having count(summarized_offense) > 0"

        map_data = client.get("nu46-gffg", query = map_query)
        time_data = client.get("nu46-gffg", query = timeline_query)
        hist_data = client.get("nu46-gffg", query = hist_query)

        map_df = pd.DataFrame(map_data)
        time_df = pd.DataFrame(time_data)
        hist_df = pd.DataFrame(hist_data)

        time_fig = px.line(time_df, x='occurred_date_or', y='count_summarized_offense', title= "Incidencts of " + ctxt + " Over Time")
        time_fig.update_xaxes(
            rangeslider_visible=True,
        )

        map_df["latitude"] = pd.to_numeric(map_df["latitude"])
        map_df["longitude"] = pd.to_numeric(map_df["longitude"])
        map_fig = px.scatter_mapbox(map_df, lat=map_df.columns[1], lon=map_df.columns[2], hover_name = "summarized_offense", color_discrete_sequence = ["fuchsia"], zoom = 10, height = 800)   
        map_fig.update_layout(mapbox_style="dark", mapbox_accesstoken="pk.eyJ1IjoiYWxhbndpbjk4IiwiYSI6ImNrY3d5OGNuaTA0bTgzMHFpamV5NzB6aTAifQ.u1TcuBVkdfy8FVCmzBB3Cw")
        map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        hist_fig = px.histogram(hist_df, x= "summarized_offense", y="count_summarized_offense", color="summarized_offense",	
            labels = {'summarized_offense': 'Incident Type', 'count_summarized_offense': 'Number of Incidents'})	
        hist_fig.update_layout( plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])	
        
        return map_fig, time_fig, hist_fig

    else:
    
        timeline_query += " where "
        map_query += " where "
        hist_query += " where "
        seen_query = False
        for i in range(len(qlist)):
            if (qlist[i] != ''):
                if (seen_query == False):
                    timeline_query = timeline_query + qlist[i]
                    map_query = map_query + qlist[i]
                    hist_query = hist_query + qlist[i]
                    seen_query = True
                else:
                    timeline_query = timeline_query + " AND " + qlist[i]
                    map_query = map_query + " AND " + qlist[i]
                    hist_query = hist_query + " AND " + qlist[i]
    
    print(hist_query)
    timeline_query += " group by occurred_date_or order by occurred_date_or"
    hist_query += " group by summarized_offense having count(summarized_offense) > 0"
    
    map_data = client.get("nu46-gffg", query = map_query)
    time_data = client.get("nu46-gffg", query = timeline_query)
    hist_data = client.get("nu46-gffg", query = hist_query)    
    
    map_df = pd.DataFrame(map_data)
    time_df = pd.DataFrame(time_data)
    hist_df = pd.DataFrame(hist_data)

    if (time_df.empty or map_df.empty or hist_df.empty):
        return {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No matching data found",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            }
        }, {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No matching data found",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            }
        }, {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No matching data found",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            }
        }
    
    else:
        time_fig = px.line(time_df, x='occurred_date_or', y='count_summarized_offense', title= "Incidencts of " + ctxt + " Over Time")
        time_fig.update_xaxes(
            rangeslider_visible=True,
        )
        map_df["latitude"] = pd.to_numeric(map_df["latitude"])
        map_df["longitude"] = pd.to_numeric(map_df["longitude"])
        map_fig = px.scatter_mapbox(map_df, lat=map_df.columns[1], lon=map_df.columns[2], hover_name = "summarized_offense", color_discrete_sequence = ["fuchsia"], zoom = 10, height = 800)   
        map_fig.update_layout(mapbox_style="dark", mapbox_accesstoken="pk.eyJ1IjoiYWxhbndpbjk4IiwiYSI6ImNrY3d5OGNuaTA0bTgzMHFpamV5NzB6aTAifQ.u1TcuBVkdfy8FVCmzBB3Cw")
        map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        hist_fig = px.histogram(hist_df, x= "summarized_offense", y="count_summarized_offense", color="summarized_offense",	
            labels = {'summarized_offense': 'Incident Type', 'count_summarized_offense': 'Number of Incidents'})	
        hist_fig.update_layout( plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])
    return map_fig, time_fig, hist_fig

@app.callback(
    Output('resetsave', 'children'),
    [Input('resetbutton','n_clicks')]
)
def contextChecker(click):
    ctx = dash.callback_context
    if (click > 0):
        if not ctx.triggered:
            print("Not Pressed")
            return False
        else:
            print("Pressed")
            return True


if __name__ == '__main__':
    app.run_server(debug=True)