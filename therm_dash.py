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
dbname = os.environ.get('THERMOSTAT_DB','thermostat.db')


class DatabaseInterface():
    """docstring for DatabaseInterface"""
    def __init__(self, dbName):
        self.dbName = dbName
        self.data = []

    def getLatest(self):
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()
        for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
            out = row
        return out

    def getNumEntries (self, numSamples=0):
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()
        if numSamples > 0:
            curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
        else:
            curs.execute("SELECT * FROM DHT_data ORDER BY timestamp")
        self.data = curs.fetchall()
        dates = []
        temps = []
        hums = []
        for row in reversed(self.data):
            dates.append(row[0])
            temps.append(row[1])
            hums.append(row[2])
        return dates, temps, hums

    def getTimeInterval (self, timerange = ("2019-01-05 12:00:00.0", "2019-01-10 12:00:00.0")):
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()
        cmd = "SELECT * FROM DHT_data WHERE timestamp BETWEEN \"{}\" AND \"{}\"".format(timerange[0], timerange[1])
        print cmd
        curs.execute(cmd)
        self.data = curs.fetchall()
        dates = []
        temps = []
        hums = []
        for row in reversed(self.data):
            dates.append(row[0])
            temps.append(row[1])
            hums.append(row[2])
        return dates, temps, hums

db = DatabaseInterface(dbname)
numRefresh = 0


app.layout = html.Div(children=[
    html.H2(children='Thermostat', style={'textAlign': 'center'}),

    html.Button('Refresh', id='button'),
    html.Div(id='output-container-button'),

    dcc.Graph(id='temp-history-graph'),

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
    out = db.getLatest()
    return 'Current Temperature: {:0.1f}  °F'.format(out[1])

@app.callback(
    dash.dependencies.Output('temp-history-graph', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('temp-history-graph', 'relayoutData')])
def update_output(n_clicks, relayoutData):
    print relayoutData
    if relayoutData and 'xaxis.range[0]' in relayoutData:
        print relayoutData['xaxis.range[0]']
        timerange = ("{}".format(relayoutData['xaxis.range[0]']).split('.')[0], 
                     "{}".format(relayoutData['xaxis.range[1]']).split('.')[0])

        print timerange
        df = db.getTimeInterval(timerange)
        # df = db.getTimeInterval()

    else:
        df = db.getNumEntries(3600)

    return {'data': [{'x': df[0], 'y': df[1], 'type': 'scatter', 'name': 'Temp'},],
            'layout': go.Layout(yaxis={'title': '°F'}) #, xaxis={'range': timerange})
            }



if __name__ == '__main__':
    app.run_server(debug=True)



