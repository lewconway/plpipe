import plotly.graph_objects as go
import plotly.io as pio


pio.templates["basic"] = go.layout.Template()

pio.templates["basic"] = {'layout': {
    'colorway': ['#0C5DA5', '#00B945', '#FF9500',
                 '#FF2C00', '#845B97', '#474747', '#9e9e9e'],
    'font_family': 'Helvetica',
    'font_color': 'black',
    'font_size': 13,
    'legend': dict(x=0.025, y=0.025, xanchor='left', yanchor='bottom',
                   bgcolor='White', borderwidth=1, bordercolor='Black'),
    'paper_bgcolor': 'white',
    'plot_bgcolor': 'white',
    'width': 350,
    'height':  265,
    'autosize': True,
    'margin': dict(l=0, r=10, b=0, t=8, pad=0),
    'xaxis': {'automargin': True,
                  'mirror': 'allticks',
                  'nticks': 10,
                  'gridcolor': 'rgb(232,232,232)',
                  'linecolor': 'rgb(36,36,36)',
                  'showgrid': False,
                  'showline': True,
                  'ticks': 'inside',
                  'minor_ticks': 'inside',
                  'title': {'standoff': 15},
                  'zeroline': False,
                  'layer': 'above traces',
                  'zerolinecolor': 'rgb(36,36,36)'},
    'yaxis': {'automargin': True,
              'tickformat': None,
              'mirror': 'allticks',
              'gridcolor': 'rgb(232,232,232)',
              'linecolor': 'rgb(36,36,36)',
              'showgrid': False,
              'showline': True,
              'ticks': 'inside',
              'minor_ticks': 'inside',
              'title': {'standoff': 15},
              'zeroline': False,
              'layer': 'above traces',
              'zerolinecolor': 'rgb(36,36,36)'}
}}
pio.templates['solid-dash'] = {'layout': {'colorway': ['#0C5DA5', '#0C5DA5', '#00B945', '#00B945',  '#FF9500',
                                                       '#FF9500',  '#FF2C00', '#FF2C00', '#845B97', '#845B97', '#474747', '#474747',  '#9e9e9e', '#9e9e9e']}}
pio.templates['outside-legend'] = {'layout': {'legend': dict(
    x=0.0, y=1.1, xanchor='left', yanchor='bottom', bgcolor='White', borderwidth=1, bordercolor='Black', )}}
pio.templates['side-outside-legend'] = {'layout': {'legend': dict(
    x=1.1, y=0, xanchor='left', yanchor='bottom', bgcolor='White', borderwidth=1, bordercolor='Black', )}}
# plpipe_templates['solid-dash']['layout'].update(
#    colorway=['#0C5DA5', '#0C5DA5', '#00B945', '#00B945',  '#FF9500', '#FF9500',  '#FF2C00', '#FF2C00', '#845B97', '#845B97', '#474747', '#474747',  '#9e9e9e', '#9e9e9e'])

template_extras = {}
template_extras['solid-dash'] = {'mode_list': ['lines'], 'dash_list': ['dash', 'solid']}

pio.templates['alternating'] = pio.templates['solid-dash']
template_extras['alternating'] = {'marker_list': ['square', 'circle']}

#plpipe_templates['outside_legend'] = copy.deepcopy(plpipe_templates['basic'])
# plpipe_templates['outside_legend']['layout']['legend'].update(dict(x=0.025, y=1.025, xanchor='left', yanchor='bottom',
#                                                                   bgcolor='White', borderwidth=1, bordercolor='Black'))
#
###plpipe_templates['solid-dash']['layout'].update({'dash': 'dash'})
