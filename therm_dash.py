# -*- coding: utf-8 -*-
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import sqlite3


from app import app, server


@server.route("/")
def MyDashApp():
    return app.index()


#app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
dbname = os.environ["THERMOSTAT_DB"]


def getLastDataEntry():
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
        out = row
    return out

def getHistData (numSamples):
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
    data = curs.fetchall()
    dates = []
    temps = []
    hums = []
    for row in reversed(data):
        dates.append(row[0])
        temps.append(row[1])
        hums.append(row[2])
    return dates, temps, hums


df = getHistData(200)

app.layout = html.Div(children=[
    html.H2(children='Thermostat', style={'textAlign': 'center'}),

    dcc.RadioItems(
        options=[
            {'label': 'up', 'value': 'up'},
            {'label': 'down', 'value': 'down'}
        ],
        value='up',
        labelStyle={'display': 'inline-block'},
        style={'margin-top': 20}
    ),

    html.Button('Refresh', id='button'),
    html.Div(id='output-container-button'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df[0], 'y': df[1], 'type': 'scatter', 'name': 'Temp'},
            ],
            'layout': go.Layout(yaxis={'title': '°F'})
        }
    ),

    html.Div(id='updatemode-output-container', style={'margin-top': 20}),
    dcc.Slider(
        id='slider-updatemode',
        min=60,
        max=80,
        step=0.5,
        value=76,
        marks={
            60: '60 °F',
            65: '65 °F',
            70: '70 °F',
            75: '75 °F',
            80: '80 °F'
        }
    ),

    dcc.RadioItems(
        options=[
            {'label': 'Heat', 'value': 'heat'},
            {'label': 'Cool', 'value': 'cool'}
        ],
        value='heat',
        labelStyle={'display': 'inline-block'},
        style={'margin-top': 20}
    )


])

@app.callback(Output('updatemode-output-container', 'children'),
              [Input('slider-updatemode', 'value')])
def display_value(value):
    return 'Desired Temparature: {:0.1f} °F'.format(value)

@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])
def update_output(n_clicks):
    out = getLastDataEntry()
    df = getHistData(100)
    return 'Current Temperature: {:0.1f}  °F'.format(out[1])


if __name__ == '__main__':
    app.run_server(debug=True)
