import pandas as pd
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash import Dash
from dash.dependencies import Input, Output, State
from datetime import datetime, timedelta

from app.db import db
from app.visualizations.layouts import init_figures, menu, filters
from app.models.covid import CovidCases, PopulationModel

def init_dashboard(server):
    dash_app = Dash(__name__, server=server, 
                        url_base_pathname='/app/covid/', 
                        external_stylesheets=[dbc.themes.BOOTSTRAP]
                        )

    dash_app.layout = html.Div([
        html.H1("COVID-19 Dashboard Netherlands"),

        dbc.Row(dbc.Col(menu.dropdown)),

        html.H2("Daily situation update"),

        dbc.Row([html.Div(id="Daily situation update"),
        init_figures.create_daily_cards()]),

        dbc.Row([filters.filters, init_figures.create_daily_graph()]),        
    ])

    init_callbacks(dash_app)

    return dash_app.server

def init_callbacks(dash_app):

    @dash_app.callback(
        Output("dropdown-place", "options"),
        [Input("dropdown-province-city", "value")],
        prevent_initial_call=True
    )
    def update_dropdown(value):
        unique_values = CovidCases.find_unique_values_in_col(value)
        return [{'label': i, 'value': i} for i in unique_values]

    @dash_app.callback(
        Output("investigation-graph", "figure"),
        [Input("button_submit", "n_clicks")],
        [State("dropdown-province-city", "value"),
        State("dropdown-place", "value"),
        State("start-date-input", "value"),
        State("end-date-input", "value"),
        State("dropdown-investigation", "value"),
        State("dropdown-investigation", "options"),
        State("dropdown-output-mode", "value")],
        prevent_initial_call=True
    )
    def update_graph(n_clicks, input_col, place, start_date, end_date, investigation_type, investigation_labels, output_mode):
        label = [x['label'] for x in investigation_labels if x['value'] == investigation_type]
        start_datetime_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime_obj = datetime.strptime(end_date, "%Y-%m-%d")
        if output_mode == "Absolute":
            df = CovidCases.find_by_timerange_and_place(start_datetime_obj, end_datetime_obj, input_col, place, investigation_type)
        elif output_mode == "Relative":
            df = PopulationModel.get_relative_cases_by_timerange_and_place(start_datetime_obj, end_datetime_obj, input_col, place, investigation_type)
            investigation_type = f"{investigation_type}_per_100000"
        
        if input_col == "Province":
            df = df.groupby(['Date_of_publication', 'Province'], as_index=False).sum()

        fig = px.area(df, x="Date_of_publication", y=investigation_type,
        hover_data=[investigation_type], text=investigation_type, title=f"{label[0]} in {place}")
        fig.update_traces(textposition='top center')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        return fig