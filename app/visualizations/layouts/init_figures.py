import pandas as pd
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from datetime import datetime, timedelta

from app.models.covid import CovidCases

def create_daily_graph():
    start_datetime_obj = datetime.strptime("2020-02-27", "%Y-%m-%d")
    end_datetime_obj = (datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    data = CovidCases.find_by_timerange(start_datetime_obj, end_datetime_obj)
    df = pd.DataFrame([(d.Date_of_publication, d.Total_reported) for d in data], 
                columns=['Date_of_publication', 'Total_reported'])
    df = df.groupby(['Date_of_publication'], as_index=False).sum()
    fig = px.area(df, x="Date_of_publication", y='Total_reported',
        hover_data=['Total_reported'],
        title=f"Total Cases over Time in the Netherlands")
    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)

    visualization = dbc.Col([
            html.Div(
                className="visualization-section",
                children=[
                    dcc.Graph(
                        id="investigation-graph",
                        config={"displayModeBar": False},
                        figure=fig
                    ),
                    dbc.Table.from_dataframe(
                        pd.DataFrame(),
                            id="table-statistics",
                        )
                ],
            ),
        ])
    return visualization

def create_daily_cards():
    positives_date, total_reported = CovidCases.get_total_positives("Total_reported")
    hospital_date, hospital_admission = CovidCases.get_total_positives("Hospital_admission")
    deceased_date, deceased = CovidCases.get_total_positives("Deceased")
    positives_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(total_reported
                    , className="card-title"),
                    html.P(
                        "People tested positive for COVID-19",
                        className="card-text",
                    ),
                    dbc.Button(f"Value published on {positives_date}", color="danger"),
                ]
            ),
    )

    hospital_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(hospital_admission, className="card-title"),
                    html.P(
                        "Hospitalizations",
                        className="card-text",
                    ),
                    dbc.Button(f"Value published on {hospital_date}",
                     color="danger"),
                ]
            ),
    )

    deaths_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(deceased, className="card-title"),
                    html.P(
                        "New deaths",
                        className="card-text",
                    ),
                    dbc.Button(f"Value published on {deceased_date}",
                     color="danger"),
                ]
            ),
    )

    cards = dbc.CardDeck(
        [
            positives_card,
            hospital_card,
            deaths_card
        ]
    )

    return cards