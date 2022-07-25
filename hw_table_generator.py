#!/srv/http/hw_table_generator/venv/bin/python3

from dash import Dash, dash_table, dcc, html, callback_context
from dash.dependencies import Input, Output, State
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from shapely import geometry
import pandas as pd


default_HW_table=[{'H': 2.22187, 'W': 0.0},
 {'H': 2.2875, 'W': 0.7820682039510287},
 {'H': 2.29375, 'W': 0.9019006081946235},
 {'H': 2.31874, 'W': 1.3127629780869565},
 {'H': 2.4375, 'W': 2.256992485282418},
 {'H': 2.44444, 'W': 2.302137876078286},
 {'H': 2.6492, 'W': 3.2573859604860407},
 {'H': 2.65312, 'W': 3.28020146023468},
 {'H': 2.8026, 'W': 3.930952490644898},
 {'H': 3.05472, 'W': 4.369960446367347},
 {'H': 3.26562, 'W': 4.405135360735843},
 {'H': 3.43394, 'W': 4.389053920886466},
 {'H': 3.4722, 'W': 3.7202815389267125},
 {'H': 3.55156, 'W': 3.3558935420965197},
 {'H': 3.67405, 'W': 3.006278260833099},
 {'H': 3.84375, 'W': 2.751033233080462},
 {'H': 3.8778, 'W': 2.6974991589966293},
 {'H': 4.10581, 'W': 2.8532817587471127},
 {'H': 4.26519, 'W': 3.242633632780215},
 {'H': 4.31562, 'W': 3.4815603125000023},
 {'H': 4.46519, 'W': 4.172869038944434},
 {'H': 4.51875, 'W': 4.166474006873294},
 {'H': 4.58968, 'W': 3.554247411392271},
 {'H': 4.73125, 'W': 3.3261752161811384},
 {'H': 4.86206, 'W': 3.212523562307421},
 {'H': 4.87873, 'W': 3.2042014824523246},
 {'H': 4.94615, 'W': 3.1876973275377725},
 {'H': 5.17255, 'W': 3.268582150292291},
 {'H': 5.25269, 'W': 3.3158536632847087},
 {'H': 5.33862, 'W': 3.3514838622159124},
 {'H': 5.5047, 'W': 3.61662883180322},
 {'H': 5.61967, 'W': 3.7971416351328093},
 {'H': 5.68866, 'W': 4.0407727906180195},
 {'H': 5.73976, 'W': 4.225222751450783},
 {'H': 5.74615, 'W': 4.225451429454062},
 {'H': 5.9135, 'W': 4.102898084758101},
 {'H': 6.26068, 'W': 3.856793801682237},
 {'H': 6.42961, 'W': 3.4692917307220674},
 {'H': 6.46019, 'W': 3.3674288313531706},
 {'H': 6.54449, 'W': 2.8412822927001526},
 {'H': 6.55292, 'W': 2.813544920084849},
 {'H': 6.66353, 'W': 2.283754077461903},
 {'H': 6.72433, 'W': 1.4974161595337714},
 {'H': 6.75021, 'W': 1.023126505456923},
 {'H': 6.78615, 'W': 0.6930377551020399},
 {'H': 6.8283, 'W': 0.0}]

default_cross_section=[
     {'X': 6.55525, 'Y': 3.05472},
     {'X': 6.17284, 'Y': 2.8026},
     {'X': 5.53946, 'Y': 2.6492},
     {'X': 4.93053, 'Y': 2.44444},
     {'X': 4.32544, 'Y': 2.31874},
     {'X': 3.90982, 'Y': 2.2875},
     {'X': 3.51294, 'Y': 2.22187},
     {'X': 3.09107, 'Y': 2.29375},
     {'X': 2.64013, 'Y': 2.4375},
     {'X': 2.275444, 'Y': 2.65312},
     {'X': 2.137945, 'Y': 3.26562},
     {'X': 2.15982, 'Y': 3.84375},
     {'X': 2.20982, 'Y': 4.31562},
     {'X': 2.334704, 'Y': 4.87873},
     {'X': 2.314264, 'Y': 5.5047},
     {'X': 2.311709, 'Y': 5.9135},
     {'X': 2.29638, 'Y': 6.42961},
     {'X': 2.619374, 'Y': 6.75021},
     {'X': 3.32448, 'Y': 6.66353},
     {'X': 3.31582, 'Y': 5.68866},
     {'X': 3.35159, 'Y': 5.17255},
     {'X': 3.48482, 'Y': 4.73125},
     {'X': 3.70669, 'Y': 4.51875},
     {'X': 4.23639, 'Y': 4.58968},
     {'X': 4.39592, 'Y': 4.94615},
     {'X': 4.33527, 'Y': 5.33862},
     {'X': 3.95968, 'Y': 5.61967},
     {'X': 3.56366, 'Y': 5.73976},
     {'X': 3.78818, 'Y': 6.55292},
     {'X': 4.27712, 'Y': 6.8283},
     {'X': 4.89532, 'Y': 6.78615},
     {'X': 5.35334, 'Y': 6.72433},
     {'X': 5.71583, 'Y': 6.54449},
     {'X': 6.13452, 'Y': 6.46019},
     {'X': 6.54478, 'Y': 6.26068},
     {'X': 6.7873, 'Y': 5.74615},
     {'X': 6.64086, 'Y': 5.25269},
     {'X': 6.45649, 'Y': 4.86206},
     {'X': 6.41586, 'Y': 4.46519},
     {'X': 5.44711, 'Y': 4.26519},
     {'X': 5.04087, 'Y': 4.10581},
     {'X': 4.70013, 'Y': 3.67405},
     {'X': 4.83482, 'Y': 3.43394},
     {'X': 5.34086, 'Y': 3.43394},
     {'X': 5.76392, 'Y': 3.55156},
     {'X': 6.37056, 'Y': 3.8778},
     {'X': 6.53116, 'Y': 3.4722}
    ]

default_fig = make_subplots(rows=1, cols=2,
                    subplot_titles=("Sample Cross Section",
                                    "Sample HW Plot"),
                    shared_yaxes=True,
                    horizontal_spacing=0.01
                    )

default_XS_df_in = pd.DataFrame(default_cross_section)
default_HW_df_in = pd.DataFrame(default_HW_table)

default_fig.add_trace(go.Scatter(x=default_XS_df_in['X'], y=default_XS_df_in['Y']),  row=1, col=1)
default_fig.add_trace(go.Scatter(x=default_HW_df_in['W'], y=default_HW_df_in['H']), row=1, col=2)
default_fig.update_layout(showlegend=False, height=800)
default_fig['layout']['xaxis']['title']='Chainage (m)'
default_fig['layout']['xaxis2']['title']='Width (m)'
default_fig['layout']['yaxis']['title']='Elevation (mAD)'

app = Dash(__name__)
col_names = ['X','Y']

app.layout = html.Div([
    html.H1('Head Width Table Generator'),
    html.Div([
        dcc.Graph(id='adding-rows-graph', figure= default_fig),
        ],
    ),
    html.Div([
        html.Div([
            html.H2('Cross Section Data'),
            html.Button('Delete most of the rows', id='delete-rows-button', n_clicks=0),
            dash_table.DataTable(
                id='adding-rows-table',
                columns=[{
                    'name': i,
                    'id': i,
                    'type': 'numeric',
                    'deletable': False,
                    'renamable': False
                } for i in col_names],
                data=default_cross_section,
                editable=True,
                row_deletable=True
            ),
        ], style={'width': '40%',  'display': 'inline-block', 'margin-left':20,},
        ),
        html.Div([
            html.H2('Generated HW Table'),
            html.Button('Generate HW Table and Plots', id='generate-HW-button', n_clicks=0),
            dash_table.DataTable(
                id='HW-rows-table',
                columns=[{
                    'name': 'H',
                    'id': 'H',
                    'type': 'numeric',
                    'deletable': False,
                    'renamable': False
                },{
                    'name': 'W',
                    'id': 'W',
                    'type': 'numeric',
                    'deletable': False,
                    'renamable': False
                    }
                ],
                data=default_HW_table,
                editable=True,
                row_deletable=True
            )], style={'width': '40%',  'display': 'inline-block', 'margin-left':20,}),
    ],className="row",
    ),html.Button('Add Row', id='editing-rows-button', n_clicks=0),
])



@app.callback(
    Output('adding-rows-table', 'data'),
    Input('editing-rows-button', component_property='n_clicks'),
    Input('delete-rows-button', component_property='n_clicks'),
    State('adding-rows-table', 'data'),
    State('adding-rows-table', 'columns')
    )
def add_row(add_row_clicks, del_row_clicks, data, columns):
    
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    
    if 'editing-rows-button' in changed_id:
        data.append({c['id']: '' for c in columns})

    if 'delete-rows-button' in changed_id:
        data=[{'X': -1, 'Y': 2},
            {'X': 0, 'Y': -1},
            {'X': 1, 'Y': 1.5},
        ]
    
    return data



@app.callback(
    Output('adding-rows-graph', 'figure'),
    Output('HW-rows-table', 'data'),
    Input('generate-HW-button', 'n_clicks'),
    State('adding-rows-table', 'data'),
    )
def display_output(n_clicks, data):
    if n_clicks > 0:
        df_in = pd.DataFrame(data).replace(r'^\s*$',np.nan,regex=True).dropna()

        x_values = df_in['X'].to_numpy()
        y_values = df_in['Y'].to_numpy()

        # make sure the polygon closes
        if x_values[-1] != x_values[0] and y_values[-1] != y_values[0]:
           # print('Added final segement to close polygon')
           x_values = np.append(x_values,x_values[0])
           y_values = np.append(y_values,y_values[0])

        xy_pairs = tuple(zip(list(x_values),list(y_values)))

        try:
            polygon = geometry.Polygon(xy_pairs)
        except Exception:
            # Make plots
            fig = make_subplots(rows=1, cols=2,
                                subplot_titles=("Cross Section",
                                                "Unable to compute bounding polygon. Make sure cross section does not self intersect"),
                                shared_yaxes=True,
                                horizontal_spacing=0.01
                                )

            fig.add_trace(go.Scatter(x=x_values, y=y_values),  row=1, col=1)
            fig.add_trace(go.Scatter(x=[], y=[]), row=1, col=2)
            fig.update_layout(showlegend=False, height=800)
            fig['layout']['xaxis']['title']='Chainage (m)'
            fig['layout']['xaxis2']['title']='Width (m)'
            fig['layout']['yaxis']['title']='Elevation (mAD)'

            HW_table = []

            return fig, HW_table


        len_x = len(x_values)
        # xy_index = np.arange(0,len_x)


        vertex = {}
        HW = {}
        # y_interpolated = {}
        y_int_coords = {}



        # for each line segment (x ind), lets find how many times y values between that range occur
        for idx, x in np.ndenumerate(x_values):
            idx = int(idx[0])
            y_value = y_values[idx]
            # x_value = x_values[idx]

            # y_before = y_values[idx-1]

            # if last value, assume the first value is the following
            if idx == (len_x-1):
                y_after = y_values[0]
                x_after = x_values[0]
            else:
                y_after = y_values[idx+1]
                x_after = x_values[idx+1]

            # print(idx,':', x,y_values[idx], 'After:' ,x_after,y_after)

            if y_value < y_after:
                lower_y = y_value
                higher_y = y_after
            else:
                lower_y = y_after
                higher_y = y_value

            # find verticies that lie on the same y as the segment
            intersect_segments = np.where(np.logical_and(y_values <= higher_y, y_values >= lower_y) == True)

            # sort the array to interpolate
            y_range_sorted = np.array([y_value,y_after])[np.array([y_value,y_after]).argsort()]
            x_range_sorted = np.array([x,x_after])[np.array([y_value,y_after]).argsort()]

            # print(intersect_segments)
            if intersect_segments[0].size > 0:
                for segment in intersect_segments[0]:
                    int_x = np.interp(y_values[segment],y_range_sorted,x_range_sorted)

                    if not segment in vertex:
                        vertex[segment] = {}

                    if not 'x' in vertex[segment]:
                        vertex[segment]['x'] = [x_values[segment]]
                        vertex[segment]['y'] = [y_values[segment]]

                    vertex[segment]['x'].append(int_x)
                    vertex[segment]['y'].append(y_values[segment])

                    y_int_coords[int_x] = y_values[segment]

            # print()


        HW_figs = []
        HW_annots = []
        HW_lines = []

        # print(vertex)

        for node, intersections in vertex.items():
            # node_x = x_values[node]
            node_y = y_values[node]

            # Skip if final node
            if node == (len_x-1):
                continue
                # Find and add 0 width node if peak / valley
                # if ((y_values[node-1] > node_y) and (y_values[node+1] > node_y)) or ((y_values[node-1] < node_y) and (y_values[node+1] < node_y)):
                #     intersections['x'].append(node_x)
                #     intersections['y'].append(node_y)
            # else:
            #     continue
                # if ((y_values[node-1] > node_y) and (y_values[0] > node_y)) or ((y_values[node-1] < node_y) and (y_values[0] < node_y)):
                #     intersections['x'].append(node_x)
                #     intersections['y'].append(node_y)



            vertex[node]['x'].sort()

            for c,v in enumerate(vertex[node]['x']):
                # print(node,c,v)
                # if ((c % 2) == 0) or c == 0:

                x0 = v

                if c == len(vertex[node]['x'])-1:
                    x1 = v
                else:
                    x1 = vertex[node]['x'][c+1]

                if node_y not in HW:
                    HW[node_y] = 0

                # Test if line is inside pollygon
                HW_line = geometry.LineString([(x0,node_y),(x1,node_y)])
                if not polygon.intersects(HW_line.centroid):
                    # print('pass')
                    continue

                if HW_line not in HW_lines:
                    HW_lines.append(HW_line)
                else:
                    continue

                W = x1-x0
                if W == 0:
                    continue

                HW[node_y] = HW[node_y]+(W)

                HW_figs.append(
                    {
                        'type': 'line',
                        'x0': x0,
                        'x1': x1,
                        'y0': node_y,
                        'y1': node_y,
                        'line': {
                            'color': 'rgb(0,0,0)',
                            'width': 1,
                            'dash': 'dot',
                            },

                    }
                )
                HW_annots.append(
                    {
                        'text': round(W,3 ),
                        'x': x0+((W)/2),
                        'y': node_y,
                        'showarrow': False,
                        'yshift': 3,

                    }
                )

        HW_df = pd.DataFrame(HW.items(), columns=['H','W']).sort_values('H')
        HW_table_out = HW_df.to_dict('records')


        # print(HW)


        # Make plots
        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=("Cross Section",
                                            "Generated HW Table"),
                            shared_yaxes=True,
                            horizontal_spacing=0.01
                            )

        fig.add_trace(go.Scatter(x=x_values, y=y_values),  row=1, col=1)
        fig.add_trace(go.Scatter(x=HW_df['W'], y=HW_df['H']), row=1, col=2)
        fig.update_layout(showlegend=False, height=800)
        fig['layout']['xaxis']['title']='Chainage (m)'
        fig['layout']['xaxis2']['title']='Width (m)'
        fig['layout']['yaxis']['title']='Elevation (mAD)'
        # fig['layout']['yaxis2']['title']='Elevation (mAD)'

        for shape in HW_figs:
            fig.add_shape(shape)

        for annot in HW_annots:
            fig.add_annotation(annot)


        return fig,HW_table_out

    else:
        return default_fig,default_HW_table

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="36363", debug=True)

