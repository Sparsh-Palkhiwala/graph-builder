from dash import dcc, html
import dash_daq as daq
from data import options, dlists

show = {'height':'auto'}
hide = {'height':'0', 'overflow':'hidden','line-height':0,'display':'block'}

main_layout = html.Div(id='main', children=[
    # dependent and independent variables (x- and y-axes)
    html.Div([
        html.Div([
            html.H6("Select x-axis"),
            dcc.Dropdown(options=options, id='x-axis', multi=True, value=['dateRep'])
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        html.Div([
            html.H6("Select y-axis"),
            dcc.Dropdown(options=options, id='y-axis', multi=True, value=['cases'])
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        html.Div([
            html.H6("Cartesian product"),
            daq.ToggleSwitch(id='cartesian-prod', value=False)
        ], style={'width': '30%', 'display': 'inline-block'})
    ], style={'marginBottom': '20px'}),
    
    # graph type selection
    html.Div([
        html.Div([
            html.H6("Select Graph Type"),
            dcc.Dropdown(
                options=[
                    {'label': 'Scatter Plot', 'value': 'scatter'},
                    {'label': 'Line Plot', 'value': 'line'},
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Histogram', 'value': 'histogram'},
                    {'label': 'Box Plot', 'value': 'box'},
                    {'label': 'Violin Plot', 'value': 'violin'}
                ],
                id='graph-type',
                value='scatter'
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'})
    ], style={'marginBottom': '20px'}),
    
    # legend options (symbol, size, color)
    html.Div([
        html.Div([
            html.H6("Select symbol"),
            dcc.Dropdown(options=options, id='symbol')
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        html.Div([
            html.H6("Select size"),
            dcc.Dropdown(options=options, id='size')
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        html.Div([
            html.H6("Select color"),
            dcc.Dropdown(options=options, id='color')
        ], style={'width': '30%', 'display': 'inline-block'})
    ], style={'marginBottom': '20px'}),
    
    # hover data selection
    html.Div([
        html.H6("Select Hover Data"),
        dcc.Dropdown(options=options, id='hover-data', multi=True)
    ], style={'marginBottom': '20px'}),
    
    # smoothing options
    html.Div([
        html.H6("Select smoothing fits"),
        dcc.RadioItems(
            options=[
                {'label': 'Whittaker', 'value': 'whittaker'},
                {'label': 'Moving Average', 'value': 'moving-average'},
                {'label': 'None', 'value': 'none'}
            ], 
            value='none', 
            id='smoother',
            style={'marginBottom': '10px'}
        ),
        html.Div(id='smoother-slider-container', children=[
            dcc.Slider(min=0, max=100, value=5, step=1, id='smoother-slider')
        ])
    ], style={'marginBottom': '20px'})
])

aliasing_layout = html.Div(id='aliasing', children=[
    html.P(id='aliasing-description', children="""
        Add aliases for long or hard to remember column names to easily enter in the dropdown boxes.
    """, style={'marginBottom': '20px'}),
    
    html.Div([
        html.Div([
            html.H6("Name"),
            dcc.Dropdown(options=options, id='name')
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        html.Div([
            html.H6("Alias"),
            dcc.Input(id='alias', value='', style={'width': '100%'})
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        html.Div([
            html.H6("Alias History"),
            dcc.Textarea(id='alias-history', value='', disabled=True, style={'width': '100%', 'height': '100px'})
        ], style={'width': '30%', 'display': 'inline-block'})
    ], style={'marginBottom': '20px'}),
    
    html.Div([
        html.Button(id='submit-alias', n_clicks=0, children='Submit', 
                   style={'backgroundColor': '#007bff', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'borderRadius': '5px'})
    ])
])

filtering_layout = html.Div(id='filtering', children=[
    html.P(id='filtering-description', children="""
        Apply filters to the dataset. For discrete variables, comma separate like "A,B" in the lower bound. 
        For continuous variables, insert lower and upper bound as integers or floats.
    """, style={'marginBottom': '20px'}),
    
    html.Div([
        html.Button("Add Filter", id="add-filter", n_clicks=0,
                   style={'backgroundColor': '#28a745', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'borderRadius': '5px', 'marginBottom': '20px'})
    ]),
    
    html.Div(id='dropdown-container', children=[], style={'marginBottom': '20px'}),
    
    html.Div(id='dropdown-container-output', children=[
        html.H6("Current Filters:"),
        dcc.Textarea(value='', id='current-filters', style={'width': '100%', 'height': '150px'})
    ])
])

for dl in dlists:
    filtering_layout.children.append(dl)
