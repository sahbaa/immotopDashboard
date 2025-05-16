import dash
from dash import dash,html,dcc
from dash import Input,Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
from dash_bootstrap_templates import ThemeSwitchAIO,template_from_url
from plotly.subplots import make_subplots
from flask_caching import Cache

# VALUE_LIST:

light_theme = dbc.themes.LUX
dark_theme = dbc.themes.CYBORG
bootstrapTheme          = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"
app                     = dash.Dash(__name__,external_stylesheets=[light_theme,bootstrapTheme])
app.layout              = dbc.Container([
                            dbc.Row([
                                html.Div([
                                    html.H3("This Is All You Need To Know About Home In LUXEMBOURG")
                                ]),
                                html.Hr(style={"border0":"1px solid #ccc"}),
                                html.Div([ThemeSwitchAIO(aio_id='themeChanger',themes=[lightTheme,darkTheme])])
                            ]),
                            dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            dcc.Dropdown(id='RS',options=[{'label':i ,'value':i}for i in ['Rent','Sale']],placeholder='select Rent Or Sale')
                                            ]),
                                        html.Div([
                                            dbc.Label("Pleased Surface",style={'padding-top':'20px'})]),
                                        html.Div([
                                            dbc.Label("From"),
                                            dcc.Input(id='min-surf',value=30,placeholder='select min surface'),
                                        
                                        html.Div([    
                                            dbc.Label("To",style={'padding':'10px'}),
                                            dcc.Input(id='max-surf',value=45,placeholder='select max surface')
                                            ])]),
                                        html.Div([
                                            dbc.Label("Pleased Bedroom",style={'padding-top':'20px'})]),
                                        html.Div([
                                            dbc.Label("From"),
                                            dcc.Input(id='min-bed',value=0,placeholder='select min bedroom'),
                                        html.Div([          
                                            dbc.Label("To",style={'padding':'10px'}),
                                            dcc.Input(id='max-bed',value=5,placeholder='select max bedroom')
                                            ])        
                                    ])],width=3),
                                    dbc.Col([
                                        dbc.Row([
                                            html.Div([
                                                dcc.Graph(id='hist-plot',figure={})
                                            ]),

                                        dbc.Row([
                                            html.Div([
                                                dbc.Card([
                                                    dbc.CardHeader('Prediction'),
                                                    dbc.CardBody([
                                                        html.H5(id='modelt-result')
                                                    ])
                                                ])
                                            ])
                                        ])
                                            
                                        ])

                                    ],width=9)
                            ])])

@app.callback([
        Output(component_id='hist-plot',component_property='figure')],

        [Input(ThemeSwitchAIO.ids.switch('themeChanger') ,"value" ),
        Input(component_id='RS',component_property="value"),
        Input(component_id='min-surf',component_property="value"),
        Input(component_id='max-surf',component_property="value"),
        Input(component_id='min-bed',component_property="value"),
        Input(component_id='max-bed',component_property="value")])
        
def declaration(tglTheme,isrent,minsurf,maxsurf,minbde,maxbed):
    template = template_from_url(light_theme if tglTheme else dark_theme)
    df = 
    return None

if __name__ == '__main__':
    app.run_server(debug=True)