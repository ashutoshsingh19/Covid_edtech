import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.graph_objects as go

from dash.dependencies import Input, Output
from functions import data_prep
from statsmodels.tsa.seasonal import seasonal_decompose

# reading the csv files

data_path = {'cou_new': 'data/coursera.csv',
             'cou_old': 'data/coursera_18_19.csv',
             'edx_new': 'data/edx.csv',
             'edx_old': 'data/edxonline_18_19.csv',
             'kha_new': 'data/khanacademy.csv',
             'kha_old': 'data/khanacademy_18_19.csv',
             'plu_new': 'data/pluralsight.csv',
             'plu_old': 'data/pluralsight_18_19.csv',
             'ski_new': 'data/skillshare.csv',
             'ski_old': 'data/skillshare_18_19.csv',
             'uda_new': 'data/udacity.csv',
             'uda_old': 'data/udacity_18_19.csv',
             'ude_new': 'data/udemy.csv',
             'ude_old': 'data/udemy_18_19.csv',
             'sky_new': 'data/skype.csv',
             'sky_old': 'data/skype_18_19.csv',
             'zoo_new': 'data/zoom.csv',
             'zoo_old': 'data/zoom_18_19.csv',
             'ted_new': 'data/TEDTalks.csv',
             'ted_old': 'data/TedTalks_18_19.csv',
             }

cou_n = pd.read_csv(data_path['cou_new'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text', 'label'])
edx_n = pd.read_csv(data_path['edx_new'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text', 'label'])
kha_n = pd.read_csv(data_path['kha_new'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text', 'label'])
plu_n = pd.read_csv(data_path['plu_new'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text', 'label'])
ski_n = pd.read_csv(data_path['ski_new'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text', 'label'])
uda_n = pd.read_csv(data_path['uda_new'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text', 'label'])
ude_n = pd.read_csv(data_path['ude_new'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text', 'label'])
sky_n = pd.read_csv(data_path['sky_new'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text', 'label'])
zoo_n = pd.read_csv(data_path['zoo_new'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text', 'label'])
ted_n = pd.read_csv(data_path['ted_new'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text', 'label'])

cou_o = pd.read_csv(data_path['cou_old'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text'])
edx_o = pd.read_csv(data_path['edx_old'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text'])
kha_o = pd.read_csv(data_path['kha_old'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text'])
plu_o = pd.read_csv(data_path['plu_old'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text'])
ski_o = pd.read_csv(data_path['ski_old'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text'])
uda_o = pd.read_csv(data_path['uda_old'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text'])
ude_o = pd.read_csv(data_path['ude_old'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text'])
sky_o = pd.read_csv(data_path['sky_old'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text'])
zoo_o = pd.read_csv(data_path['zoo_old'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text'])
ted_o = pd.read_csv(data_path['ted_old'], parse_dates=['timestamp'],
                    usecols=['username', 'timestamp', 'likes', 'replies', 'retweets', 'text'])

dict_main = {'Coursera': cou_n,
             'edX': edx_n,
             'Khan Academy': kha_n,
             'Pluralsight': plu_n,
             'Skillshare': ski_n,
             'Udacity': uda_n,
             'Udemy': ude_n,
             'Skype': sky_n,
             'Zoom': zoo_n,
             'TED Talks': ted_n}

app = dash.Dash(__name__)

data = list(dict_main.keys())  # keys for the dataset values
channels = dict_main[data[0]]  # the_data_sets

channels = data_prep(channels)

app.layout = html.Div([
    html.H1('COVID Edu-Tech', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.Label([
                "Select Platform",
                dcc.Dropdown(
                    id='data-dropdown',
                    options=[{'label': label, 'value': label} for label in data],
                    value=list(dict_main.keys())[0],
                    multi=False,
                    searchable=False,
                    clearable=False)],
                style={'width': '20%', 'display': 'inline-block'},
                className='three columns'),
            html.Label([
                "Select Parameter",
                dcc.Dropdown(
                    id='data-label',
                    options=[{'label': 'Likes', 'value': 'likes'},
                             {'label': 'Replies', 'value': 'replies'},
                             {'label': 'Retweets', 'value': 'retweets'},
                             {'label': 'No. of Tweets', 'value': 'tweet_counter'}],
                    value='likes',
                    multi=False,
                    clearable=False,
                    searchable=False)
            ],
                style={'width': '15%', 'display': 'inline-block'},
                className='three columns'),
            html.Label([
                "Tweets made by",
                dcc.Dropdown(
                    id='select-username',
                    value=1,
                    multi=False,
                    clearable=False,
                    searchable=False)
            ],
                style={'width': '15%', 'display': 'inline-block'},
                className='three columns'),
            html.Label([
                "Choose Frequency to apply Moving average",
                dcc.Slider(
                    id='frequency-slider',
                    min=1,
                    max=25,
                    step=1,
                    value=10,
                    marks={1: '1',
                           5: '5',
                           10: '10',
                           15: '15',
                           20: '20',
                           25: '25'}
                ),
                html.Div(id='slider-text', className='six columns offset-by-three')
            ],
                className='five columns'),
        ], className='row'),
    ]),
    html.Div([
        html.Div([
            dcc.Graph(
                id='my-graph',
            )
        ], className='six columns'),
        html.Div([
            dcc.Graph(
                id='subplot'
            )
        ], className='six columns')
    ], style={'width': '100%'}),

    html.Div([
        html.Div([
            dcc.Graph(
                id='graph3',
            )
        ], className='twelve columns'),
        html.Div([
            dcc.Graph(id='graph4')
        ], className='eight columns'),
        ]),
    html.Div([
        dcc.Markdown("""**Tweet**"""),
        html.Pre(
            id='hover-data',
            className='normal'
            )
        ], className='two columns')
    ], className='row')


@app.callback(Output('select-username', 'options'),
              [Input('data-dropdown', 'value')])
def update_drop(selected_dropdown1):
    options = [{'label': str(selected_dropdown1) + ' handle', 'value': 1},
               {'label': 'Users', 'value': 2},
               {'label': 'Both', 'value': 3}]
    return options


@app.callback(Output('slider-text', 'children'),
              [Input('frequency-slider', 'value')])
def slider_text(slid):
    return 'Moving average over {} weeks'.format(slid)


@app.callback(Output('my-graph', 'figure'),
              [Input('data-dropdown', 'value'),
               Input('data-label', 'value'),
               Input('select-username', 'value'),
               Input('frequency-slider', 'value')])
def update_figure(selected_dropdown1, selected_dropdown2, val, fr):
    dropdown = {'Coursera': cou_o,
                'edX': edx_o,
                'Khan Academy': kha_o,
                'Pluralsight': plu_o,
                'Skillshare': ski_o,
                'Udacity': uda_o,
                'Udemy': ude_o,
                'Skype': sky_o,
                'Zoom': zoo_o,
                'TED Talks': ted_o}
    df = dropdown[selected_dropdown1]
    if val == 1:
        df1 = df[df['username'] == selected_dropdown1]
    elif val == 2:
        df1 = df[df['username'] != selected_dropdown1]
    else:
        df1 = df
    test = data_prep(df1)
    test_i = seasonal_decompose(test[selected_dropdown2], model='additive', period=fr)
    t1 = pd.DataFrame(test_i.trend)
    t1.index = t1.index.to_timestamp().to_pydatetime()

    figure = {
        'data': [
            {'x': t1.index,
             'y': t1['trend'],
             'range_x': [t1.index.min(), t1.index.max()],
             'type': 'scatter',
             'mode': 'marker',
             'opacity': 0.7
             }],
        'layout': {
            'title': 'Trend analysis of 2018-19 period for {}'.format(selected_dropdown2),
            'xaxis': {
                'title': 'Timeline'
            }
        }
    }
    return figure


@app.callback(Output('subplot', 'figure'),
              [Input('data-dropdown', 'value'),
               Input('data-label', 'value'),
               Input('select-username', 'value'),
               Input('frequency-slider', 'value')])
def update_figure(selected_dropdown1, selected_dropdown2, val, fr):
    dropdown = {'Coursera': cou_n,
                'edX': edx_n,
                'Khan Academy': kha_n,
                'Pluralsight': plu_n,
                'Skillshare': ski_n,
                'Udacity': uda_n,
                'Udemy': ude_n,
                'Skype': sky_n,
                'Zoom': zoo_n,
                'TED Talks': ted_n}
    df = dropdown[selected_dropdown1]
    if val == 1:
        df1 = df[df['username'] == selected_dropdown1]
    elif val == 2:
        df1 = df[df['username'] != selected_dropdown1]
    else:
        df1 = df
    test = data_prep(df1)
    test_i = seasonal_decompose(test[selected_dropdown2], model='additive', period=fr)
    t1 = pd.DataFrame(test_i.trend)
    t1.index = t1.index.to_timestamp().to_pydatetime()

    figure = {
        'data': [
            {'x': t1.index,
             'y': t1['trend'],
             'range_x': [t1.index.min(), t1.index.max()],
             'type': 'scatter',
             'mode': 'marker',
             'opacity': 0.7
             }],
        'layout': {
            'title': 'Trend analysis of 2019-20 period for {}'.format(selected_dropdown2),
            'xaxis': {
                'title': 'Timeline'
            }
        }
    }
    return figure


@app.callback([Output('graph3', 'figure'),
               Output('graph4', 'figure')],
              [Input('data-dropdown', 'value'),
               Input('select-username', 'value')])
def update_figure(selected_dropdown1, val):
    dropdown = {'Coursera': cou_n,
                'edX': edx_n,
                'Khan Academy': kha_n,
                'Pluralsight': plu_n,
                'Skillshare': ski_n,
                'Udacity': uda_n,
                'Udemy': ude_n,
                'Skype': sky_n,
                'Zoom': zoo_n,
                'TED Talks': ted_n}
    df = dropdown[selected_dropdown1]

    if val == 1:
        df1 = df[df['username'] == selected_dropdown1]
        var = selected_dropdown1 + ' handle'
    elif val == 2:
        df1 = df[df['username'] != selected_dropdown1]
        var = 'Users'
    else:
        df1 = df
        var = 'Both (Platform and user)'

    test = data_prep(df1)
    test.index = test.index.to_timestamp().to_pydatetime()

    trace1 = go.Bar(
        x=test.index,
        y=test['tweet_counter'] - test['label'],
        name='Non Covid',
        hovertext=test['tweet_counter'] - test['label']
    )
    trace2 = go.Bar(
        x=test.index,
        y=test['label'],
        name='Covid',
        hovertext=test['label']
    )

    figure1 = go.Figure(
        data=[trace1, trace2],
        layout=go.Layout(
            barmode='stack',
            title='Analysis for Covid and Non-Covid related tweets from {} on a weekly basis '.format(var),
            # paper_bgcolor='rgba(48, 48, 48, 1)',
            plot_bgcolor='white'
        ))

    df2 = df1[df1['label']==1]

    wc = [len(text) for text in df2['text']]
    time = [tim for tim in df2['timestamp']]

    trace3 = go.Scatter(
        x=time,
        y=wc,
        mode='markers',
        marker={
            'color': '#ff471a',
            'size': wc,
            'sizemode': 'area',
            'sizeref': 2. * max(wc) / (40. ** 2),
            'sizemin': 4})

    figure2 = go.Figure(
        data=[trace3],
        layout=go.Layout(plot_bgcolor='white', title='Covid related tweets on timeline')
    )

    return figure1, figure2


@app.callback(
    Output('graph4', 'hoverData'),
    [Input('data-dropdown', 'value'),
     Input('select-username', 'value')])
def update_hover(val1, val2):
    return None

@app.callback(
    Output('hover-data', 'children'),
    [Input('graph4', 'hoverData'),
     Input('data-dropdown', 'value'),
     Input('select-username', 'value')
     ])
def display_hover_data(hoverData, selected_dropdown1, val):

    dropdown = {'Coursera': cou_n,
                'edX': edx_n,
                'Khan Academy': kha_n,
                'Pluralsight': plu_n,
                'Skillshare': ski_n,
                'Udacity': uda_n,
                'Udemy': ude_n,
                'Skype': sky_n,
                'Zoom': zoo_n,
                'TED Talks': ted_n}
    df = dropdown[selected_dropdown1]

    if val == 1:
        df1 = df[df['username'] == selected_dropdown1]
    elif val == 2:
        df1 = df[df['username'] != selected_dropdown1]
    else:
        df1 = df

    if hoverData is None:
        return 'Hover over the graph to overview doc'
    else:
        val_tem = hoverData['points'][0]['x']
        ret = df1[df1['timestamp'] == val_tem]['text'].values[0]
        u = df1[df1['timestamp'] == val_tem]['username'].values[0]
        return 'Username: ' + u + '\n' + ret


if __name__ == '__main__':
    app.run_server(debug=True)
