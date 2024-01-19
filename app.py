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

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

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
    [
        dbc.CardImg(id = 'onoff_img',
            src="https://cdnl.iconscout.com/lottie/premium/thumb/air-conditioner-5558928-4647174.gif",
            top=True,
            style={"opacity": 0.3},
        ),
        dbc.CardImgOverlay(
            dbc.CardBody(
                [
                    html.H4("Aircon Status", className="card-title"),
                    html.H5(children = [],
                        id = "h5-button-value",
                        className="card-text",
                    ),
                    on_off_button,
                ],
            ),
        ),
    ],
    style={"width": "18rem"},
)

app.layout = html.Div([
    html.H1(children='Daikin SkyFi AirCon Unit', style={'textAlign':'center'}),
    intervals_input, 
    html.Div([
        dbc.Row(
            [ dbc.Col(card)
                # dbc.Col(html.Div(f"Aircon is {on_off_options[int(aircon_values['opmode'])]}"),width=4),
                # dbc.Col(html.Div("Row 0, Column 1"),width=4),
                # dbc.Col(html.Div("Row 0, Column: 2"),width=4)
            ]
        ),
        dbc.Row(
            id = 'zones-cards'
            #nz=8&zone1=Theatre&zone2=Gym&zone3=Family&zone4=Beds&zone5=Zone%205&zone6=Zone%206&zone7=Zone%207&zone8=Zone%208
            # [ 
            #     dbc.Col(dbc.Card(
            #     [dbc.CardBody(["Theatre"])]), width = 3),
            #     dbc.Col(dbc.Card(
            #     [dbc.CardBody(["Gym"])]), width = 3),
            #     dbc.Col(dbc.Card(
            #     [dbc.CardBody(["Family"])]), width = 3),
            #     dbc.Col(dbc.Card(
            #     [dbc.CardBody(["Bedrooms"])]), width = 3)

            # ]
        ), 
        # html.Br, html.Br, html.Br, html.Br, 
        html.P(children = [], id = "current-status" )
        
        ])
])




@app.callback(
    [Output('current-status', 'children'), Output('h5-button-value', 'children'), Output('zones-cards', 'children')],
    [Input(intervals_input, 'n_intervals')], # T8: Change this to have the dcc.store data as input
)
def update_current_status(n):        # T8: The input va=riable should be changed to something like json_clean_data
    aircon.update()
    aircon_values = {i.split("=")[0]:i.split("=")[1] for i in aircon.current_data}
    
    cards = []
    for z in ["Theatre", "Gym", "Family","Beds"]:
        if z in aircon._zones:
            c = dbc.Col(dbc.Card([dbc.CardBody([z])], color="success", inverse = True), width = 3, style={"opacity": 1 if aircon._operation_mode else 0.3})
            cards.append(c)
        else:
            cards.append(dbc.Col(dbc.Card([dbc.CardBody([z])], color="secondary", inverse = True), width = 3, style={"opacity": 0.3}))
        
        
    return " ".join(aircon_values), f"Aircon is {on_off_options[int(aircon_values['opmode'])]}", cards

    
    

@app.callback(
    [Output(on_off_button, 'children'),Output('onoff_img', 'src')],
    [Input(on_off_button, 'n_clicks')],
)
def toggle_power(n):
    current_mode = aircon._operation_mode
    print(f'Aircon is {current_mode}')
    print(n)
    if n is not None and n > 0:
        new_mode = int(not current_mode )# Reverse it. 
        aircon.set_values(toggle_power = new_mode)
        print(f'Aircon is {new_mode}')
    else:
        pass
    
    button = dbc.Button("Turn Off" if aircon._operation_mode else "Turn On" , color="primary" if aircon._operation_mode else "warning")
    card_img = "https://cdnl.iconscout.com/lottie/premium/thumb/air-conditioner-5558928-4647174.gif" if aircon._operation_mode else "https://miro.medium.com/v2/resize:fit:1400/1*Gvgic29bgoiGVLmI6AVbUg.gif" 
    
    return button, card_img

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug = False)
    
    
