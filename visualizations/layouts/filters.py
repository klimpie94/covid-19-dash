import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

filters = dbc.Col([
                html.Div(
                    className="left-col",
                    children=[
                        html.Div(
                            className="province-city-selection",
                            children=[
                                html.H5("Choose a Province or City"),
                                dcc.Dropdown(
                                options=[
                                    {"label": "Province", "value": "Province"},
                                    {"label": "City", "value": "Municipality_name"}],
                                placeholder="Select one",
                                multi=False,
                                id="dropdown-province-city",
                                persistence="string",
                                persistence_type="local",
                                ),
                            ]
                        ),
                        html.Div(
                            className="place-selection",
                            children=[
                                html.Br(),
                                dcc.Dropdown(
                                options=[],
                                placeholder="Select one",
                                multi=False,
                                id="dropdown-place",
                                persistence="string",
                                persistence_type="local",
                                ),
                                html.Hr()
                            ]
                        ),
                        dbc.Row([
                            dbc.Col([
                                html.H5("Start Date"),
                                dcc.Input(id="start-date-input", type="date")
                            ]),
                            dbc.Col([
                                html.H5("End Date"),
                                dcc.Input(id="end-date-input", type="date")
                            ])
                        ]),
                        html.Div(
                            className="investigation-type",
                            children=[
                                html.Hr(),
                                html.H5("Investigation type"),
                                dcc.Dropdown(
                                options=[
                                    {"label": "Positive Cases over Time", "value": "Total_reported"},
                                    {"label": "Hospital Admissions over time", "value": "Hospital_admission"},
                                    {"label": "Deceased over Time", "value": "Deceased"}
                                    ],
                                placeholder="Select Investigation",
                                multi=False,
                                id="dropdown-investigation",
                                persistence="string",
                                persistence_type="local",
                                optionHeight=50
                                ),
                                html.Br(),
                                dcc.Dropdown(
                                options=[
                                    {"label": "Absolute Values", "value": "Absolute"},
                                    {"label": "Relative Value per 100.000 Residents", "value": "Relative"}
                                    ],
                                placeholder="Select Output Mode",
                                multi=False,
                                id="dropdown-output-mode",
                                persistence="string",
                                persistence_type="local",
                                optionHeight=50
                                ),
                            ],
                        ),
                        html.Div(
                            id="submit-button-insights",
                            children=[
                                html.Br(),
                                html.Button("Submit", id="button_submit"),
                            ],
                        ),
                    ]
                )
            ], width=3)