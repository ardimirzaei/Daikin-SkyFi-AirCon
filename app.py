# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 14:50:52 2024

@author: ArdiMirzaei
"""


from dash import dcc, Dash, html, dcc, callback, Output, Input
# import plotly.express as px
# import pandas as pd
import dash_bootstrap_components as dbc
import os
from dotenv import load_dotenv
import flask

from SkyFi import SkyFi


load_dotenv()

PASSWORD = os.environ.get("PASSWORD")
AC_IP_ADDRESS = os.environ.get("AC_IP_ADDRESS")

external_stylesheets = [dbc.themes.BOOTSTRAP]

server = flask.Flask(__name__) # define flask app.server
app = Dash(__name__, server=server,  external_stylesheets=external_stylesheets)


intervals_input = dcc.Interval(interval=5000, n_intervals=0)
aircon = SkyFi("Daikin", "Celsius", AC_IP_ADDRESS, PASSWORD)
aircon.update()
aircon_values = {i.split("=")[0]:i.split("=")[1] for i in aircon.current_data}
on_off_options = {0:'OFF', 1:'ON'}

current_status_output = html.Div()
on_off_button = html.Div()

card = dbc.Card(
    [dbc.CardHeader( html.H4("Aircon Status", className="card-title")), 
        dbc.CardImg(id = 'onoff_img',
            src="https://cdnl.iconscout.com/lottie/premium/thumb/air-conditioner-5558928-4647174.gif",
            top=True,
            style={"opacity": 0.3},
        ), dbc.CardBody(
                [
                    html.H5(children = [],
                        id = "h5-button-value",
                        className="card-text",
                    ),
                    on_off_button,
                ],
            ),
    ],
    style={"width": "18rem"},
)

temperature = html.Div()
set_temperature = html.Div()
                 
app.layout = html.Div([
    html.H1(children='Daikin SkyFi AirCon Unit', style={'textAlign':'center'}),
    intervals_input, 
    html.Div([
        dbc.Row(
            [ dbc.Col(card)
             , dbc.Col(set_temperature)
             , dbc.Col(temperature)
            ], 
            className="flex-md-fill"
        ),
        dbc.Row(
            id = 'zones-cards'
        ), 
        # html.Br, html.Br, html.Br, html.Br, 
        html.P(children = [], id = "current-status" )
        
        ])
])




@app.callback(
    [
     Output('current-status', 'children'), 
     Output('h5-button-value', 'children'), 
     Output('zones-cards', 'children'), 
     Output(temperature, 'children')
     ],
    [Input(intervals_input, 'n_intervals')], 
)
def update_current_status(n):        
    aircon.update()
    aircon_values = {i.split("=")[0]:i.split("=")[1] for i in aircon.current_data}
    
    cards = []
    for z in ["Theatre", "Gym", "Family","Beds"]:
        if z in aircon._zones:
            # c = dbc.Col(dbc.Card([dbc.CardBody([z])], color="success", inverse = True), width = 3, style={"opacity": 1 if aircon._operation_mode else 0.3})
            # cards.append(c)
            b = dbc.Button(id = f'btn-{z}', children = z, color="success", style={"opacity": 1 if aircon._operation_mode else 0.3}, className="flex-md-fill")
            cards.append(b)
        else:
            # cards.append(dbc.Col(dbc.Card([dbc.CardBody([z])], color="secondary", inverse = True, outline = True), width = 3, style={"opacity": 0.3}))
            b = dbc.Button(id = f'btn-{z}', children =  z, color="secondary", outline = True, style={"opacity":0.3}, className="flex-md-fill")
            cards.append(b)
        
    aircon_temp = dbc.Card([
        dbc.CardHeader(html.H4("Temperature")), 
        dbc.CardBody(html.P([
            f"Aircon: {aircon_values['settemp']}", html.Br(), f"Room: {aircon_values['roomtemp']}", html.Br(), f"Outside: {aircon_values['outsidetemp']}"]), className="card-text")
    ])
    
        
    cards = html.Div(cards, className="d-grid gap-2 d-md-flex justify-content-md-evenly")    
    return " ".join([f"{i}:{j}" for i,j in aircon_values.items()]), f"Aircon is {on_off_options[int(aircon_values['opmode'])]}", cards, aircon_temp

    
    

@app.callback(
    [Output(on_off_button, 'children'),Output('onoff_img', 'src')],
    [Input(on_off_button, 'n_clicks')],
)
def toggle_power(n):
    current_mode = aircon._operation_mode
    # print(f'Aircon is {current_mode}')
    # print(n)
    if n is not None and n > 0:
        new_mode = int(not current_mode )# Reverse it. 
        aircon.set_values(toggle_power = new_mode)
        print(f'Aircon is {new_mode}')
    else:
        pass
    
    button = dbc.Button("Turn Off" if aircon._operation_mode else "Turn On" , color="primary" if aircon._operation_mode else "warning", className="flex-md-fill")
    card_img = "https://cdnl.iconscout.com/lottie/premium/thumb/air-conditioner-5558928-4647174.gif" if aircon._operation_mode else "https://miro.medium.com/v2/resize:fit:1400/1*Gvgic29bgoiGVLmI6AVbUg.gif" 
    
    return button, card_img



@app.callback(
    [Output('btn-Theatre', 'color')],
    [Input('btn-Theatre', 'n_clicks')],
)
def toggle_zone(n):
    # print(n)
    if n > 0:        
        return "success"
    else:
        return "secondary"
    
    return 

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug = True)
    
    
