from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from verdin import tinybird
import json

# Create a Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

# Get Tinybird token and host from local
with open('.tinyb') as tb:
    data = json.load(tb)
    tb_token = data['token']
    tb_host = data['host']

# Create a Tinybird Client using Verdin SDK and passing token and host
tb_client = tinybird.Client(
    token=tb_token, api=tb_host)

instruments = tb_client.pipe("instruments_pipe_5973")
instrument_data_by_minute = tb_client.pipe("instrument_data_processed_0377_pipe_9625")

# meals = tb_client.pipe("meals")
# flight_bookings_by_minute = tb_client.pipe("flight_bookings_by_minute")
# age_distribution = tb_client.pipe("age_distribution")
# extra_bags_count = tb_client.pipe("extra_bags_count")
# priority_boarding_distribution = tb_client.pipe(
#     "priority_boarding_distribution")

# Get airlines and meal options from Tinybird API to populate dropdown filter options
instruments: tinybird.PipeJsonResponse = instruments.query()
instruments_options = pd.json_normalize(instruments.data)
print(instruments_options)


# meals: tinybird.PipeJsonResponse = meals.query()
# meal_options = pd.json_normalize(meals.data)

app.layout = html.Div(style={'padding': '2rem', 'height': '100vh'}, children=[
    html.Div(style={'height': '15%'}, children=[
        html.H1(children='A real-time Python dashboard built with Tinybird and Dash',
                style={
                    'textAlign': 'left',
                    'paddingLeft': '5rem'
                }
                ),
        html.Div(style={'display': 'flex', 'width': '100%', 'paddingLeft': '5rem', 'marginTop': '2rem'},
                 children=[
            dcc.Dropdown(instruments_options.instrument_id,
                         multi=True,
                         id='instrument-selector',
                         placeholder="Filter by intrument_id(s)",
                         style={'width': 'auto',
                                'minWidth': '250px',
                                'margin': '0.1em'}
                         ),
        #     dcc.Dropdown(meal_options.meal_preference,
        #                  id='meal-selector',
        #                  placeholder="Filter by meal preference",
        #                  style={'width': 'auto',
        #                         'minWidth': '250px',
        #                         'margin': '0.1em'}
        #                  ),
        #      html.Div(style={'maxWidth': '100px', 'padding': '0.5em'}, children=[
        #          html.P(children='Lookback', style={'margin': 'auto'})
        #      ],
        #     ),
        #     dcc.Input(id='lookback-input',
        #               type="number",
        #               debounce=True,
        #               value=1,
        #               style={'maxWidth': '50px',
        #                      'margin': '0.1em',
        #                      'border': '1px solid #ccc',
        #                      'borderRadius': '4px'
        #                      }
        #               ),
        #     html.Div(style={'maxWidth': '100px', 'padding': '0.5em'}, children=[
        #         html.P(children='hrs', style={'margin': 'auto'})
        #     ],
        #     ),
        ]
        ),
    ]),
    dcc.Graph(style={'height': '45%'}, id='instrument-data-chart'),
    # html.Div(style={'display': 'flex', 'height': '45%', 'paddingLeft': '4rem'}, children=[
    #     dcc.Graph(style={'width': '33%'}, id='age-chart'),
    #     dcc.Graph(style={'width': '33%'}, id='extra-bags-chart'),
    #     dcc.Graph(style={'width': '33%'}, id='priority-boarding-chart')
    # ]),
    dcc.Interval(interval=60000,
                 n_intervals=0,
                 id='refresh-interval'
                 )
])


@callback(
    Output('instrument-data-chart', 'figure'),
    [Input('instrument-selector', 'value'),
     Input('refresh-interval', 'n_intervals')]
)

def update_time_series_graph(instruments, n):
    print(instruments)
    if instruments:
        instruments = ','.join(instruments)
    response: tinybird.PipeJsonResponse = instrument_data_by_minute.query({
        "instruments": instruments
    })
    df = response.data.copy()
    fig = px.line(df,
                  x='minute',
                  y='avg_temp',
                  color='instrument_id',
                  labels={'minute': 'Minute',
                          'avg_temp': 'Average Temperature', 'instrument_id': 'Instrument'},
                  title='Average Readings')
    return fig


# @callback(
#     Output('age-chart', 'figure'),
#     [Input('airline-selector', 'value'),
#      Input('meal-selector', 'value'),
#      Input('lookback-input', 'value'),
#      Input('refresh-interval', 'n_intervals')]
# )
# def update_age_chart(airlines, meal, lookback, n):
#     if airlines:
#         airlines = ','.join(airlines)
#     response: tinybird.PipeJsonResponse = age_distribution.query({
#         "airlines": airlines,
#         "meal_preference": meal,
#         "lookback": lookback
#     })
#     df = response.data.copy()
#     fig = px.pie(df,
#                  values='count',
#                  names='age_grouping',
#                  hole=0.5,
#                  labels={'count': 'Total', 'age_grouping': 'Age Group'},
#                  title='Age Distribution of Passengers'
#                  )
#     return fig


# @callback(
#     Output('extra-bags-chart', 'figure'),
#     [Input('airline-selector', 'value'),
#      Input('meal-selector', 'value'),
#      Input('lookback-input', 'value'),
#      Input('refresh-interval', 'n_intervals')]
# )
# def update_extra_bags_chart(airlines, meal, lookback, n):
#     if airlines:
#         airlines = ','.join(airlines)
#     response: tinybird.PipeJsonResponse = extra_bags_count.query({
#         "airlines": airlines,
#         "meal_preference": meal,
#         "lookback": lookback
#     })
#     df = response.data.copy()
#     fig = px.bar(df,
#                  x='extra_bags',
#                  y='count',
#                  color='airline',
#                  labels={'count': '# of Passengers',
#                          'extra_bags': '# of Extra Bags',
#                          'airline': 'Airline'},
#                  title='Number of Extra Bags',
#                  )
#     return fig


# @callback(
#     Output('priority-boarding-chart', 'figure'),
#     [Input('airline-selector', 'value'),
#      Input('meal-selector', 'value'),
#      Input('lookback-input', 'value'),
#      Input('refresh-interval', 'n_intervals')]
# )
# def update_priority_boarding_chart(airlines, meal, lookback, n):
#     if airlines:
#         airlines = ','.join(airlines)
#     response: tinybird.PipeJsonResponse = priority_boarding_distribution.query({
#         "airlines": airlines,
#         "meal_preference": meal,
#         "lookback": lookback
#     })
#     df = response.data.copy()
#     fig = px.bar(df,
#                  y='airline',
#                  x='priority_boarding_percent',
#                  color='airline',
#                  labels={'priority_boarding_percent': '% Priority',
#                          'airline': 'Airline'},
#                  title='Priority Boarding Distribution',
#                  orientation='h'
#                  )
#     return fig


if __name__ == '__main__':
    app.run(debug=True)