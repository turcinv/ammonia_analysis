# Version 1.01 23.06.2023
from analysis.ammonia import Ammonia
from analysis.systems import systems
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

DEBUG = True

app = Dash(__name__)

system_keys = list(systems.keys())

app.layout = html.Div([
    dcc.Tabs(
        id='dropdown', value=str(system_keys[0]),
        children=[
            dcc.Tab(id=str(system_keys[i]),
                    label=str(system_keys[i]),
                    value=str(system_keys[i]),
                    style={'font-size': '15px',
                           'padding': "10px",
                           'text-align': 'center',
                           },
                    selected_style={'font-size': '15px',
                                    'padding': "10px",
                                    'text-align': 'center',
                                    'background-color': 'lightgray',
                                    }) for i in range(len(system_keys))
        ], style={
            "display": "flex",
            "justify-content": "center",
            "width": "100%",
            "align-items": "center"}
    ),
    html.Div(id='output-container'),

], style={
    "align-items": "center",
    'flex-direction': 'column',
    'background-color': 'lightgray'}
)


@app.callback(
    Output('output-container', 'children'),
    Input('dropdown', 'value')
)
def update_output(value):
    children = [
        html.Div([
            dcc.Graph(figure=Ammonia(int(value)).generate_ener_figure()),
        ], style={
            "display": "flex",
            "justify-content": "center",
            "width": "100%",
            "align-items": "center",
            'flex-direction': 'column',
        },
        )]
    return children


if __name__ == '__main__':
    if DEBUG:
        app.run_server(debug=True)
    else:
        for ammonia in system_keys:
            print(Ammonia(ammonia))
            Ammonia(ammonia).save_figure()
        app.run_server()
