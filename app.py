# -*- coding: utf-8 -*-
"""
Copyright (C) 2020 David Ollodart
GNU General Public License <https://www.gnu.org/licenses/>.
"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL, MATCH
import pandas as pd
from data import df, options
from layouts import *
from fig_updater import fig_updater
from filter import assign_filter, apply_filter
from smooth import assign_smooth
from alias import assign_alias
from nav import assign_nav

def create_dash_app():
    fig = fig_updater(df, xs=['dateRep'], ys=['cases'], graph_type='scatter') 
    graph_layout = dcc.Graph(figure=fig, id='plot')
    app = dash.Dash(suppress_callback_exceptions=True)
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False, pathname='/main'),
        html.H1(children='Plotly Graph Builder', style={'textAlign': 'center', 'marginBottom': '30px'}),
        
        # Navigation
        html.Div([
            dcc.Link('Main', href='/main', style={'marginRight': '20px', 'fontSize': '16px', 'textDecoration': 'none'}),
            dcc.Link('Filtering', href='/filtering', style={'marginRight': '20px', 'fontSize': '16px', 'textDecoration': 'none'}),
            dcc.Link('Aliasing', href='/aliasing', style={'fontSize': '16px', 'textDecoration': 'none'})
        ], style={'textAlign': 'center', 'marginBottom': '30px', 'padding': '10px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),
        
        # All layouts (navigation will show/hide them)
        html.Div(id='page-content', children=[
            main_layout,
            aliasing_layout, 
            filtering_layout,
            html.Hr(style={'margin': '30px 0'}),
            graph_layout
        ], style={'padding': '20px'})
    ])
    return app

app = create_dash_app()
app = assign_nav(app)
app = assign_filter(app)
app = assign_smooth(app)
app = assign_alias(app)

@app.callback(
    [Output('plot', 'figure'),
     Output('current-filters', 'value')],
    [Input('x-axis', 'value'),
     Input('y-axis', 'value'),
     Input('symbol', 'value'),
     Input('size', 'value'),
     Input('color', 'value'),
     Input('hover-data', 'value'),
     Input('cartesian-prod','value'),
     Input('graph-type', 'value'),
     Input('smoother', 'value'),
     Input('smoother-slider', 'value'),
     Input({'type': 'filter-update', 'index': ALL}, 'n_clicks')
     ],
    [State({'type': 'filter-dropdown', 'index': ALL}, 'value'),
         State({'type': 'filter-lb', 'index': ALL}, 'value'),
         State({'type': 'filter-ub', 'index': ALL}, 'value'),
         State('current-filters', 'value')])
def all_figure_callbacks(x, y, 
        symbol, size, color, hover_data, 
        cartesian_prod, graph_type,
        smoother, smoother_slider,
        filter_nclicks, filter_fields, filter_lbs, filter_ubs, filter_history):

    has_filter = False
    nnone = []
    for i in range(len(filter_fields)):
        if filter_fields[i] is not None:
            has_filter = True
            nnone.append((filter_fields[i], filter_lbs[i], filter_ubs[i]))

    if has_filter:
        f, l, u = zip(*nnone)
        gbl, filter_history_update = apply_filter(f, l, u)
        filter_history += f'{filter_nclicks}\n' + filter_history_update
    else:
        gbl = [True]*len(df)

    fig = fig_updater(df[gbl], x, y,
            symbol=symbol,
            size=size,
            color=color,
            hover_data=hover_data,
            cartesian_prod=cartesian_prod,
            graph_type=graph_type,
            smoother=smoother,
            smoother_parameter=smoother_slider)
    fig.update_layout(transition_duration=500)
    return fig, filter_history

if __name__ == '__main__':
    app.run(debug=True)
