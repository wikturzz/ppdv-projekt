import dash
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

from storage import get_storage

global patient_id


def get_data():
    if patient_id in get_storage():
        patient_data = get_storage()[patient_id]
        timestamps = np.array(patient_data["timestamps"])
        values = np.array(patient_data["values"])
        anomalies = np.array(patient_data["anomalies"])
    else:
        timestamps = np.array([0])
        values = np.array([[0, 0, 0, 0, 0, 0]])
        anomalies = np.array([False, False, False, False, False, False])

    # Create anomalies list
    anomaly_timestamps = [[], [], [], [], [], []]
    anomaly_values = [[], [], [], [], [], []]
    for i in range(0, len(timestamps) - 1):
        if anomalies[i].any():
            j = 0
            for anomaly in anomalies[i]:
                if anomaly:
                    anomaly_timestamps[j].append(timestamps[i])
                    anomaly_values[j].append(values[i, j])
                j += 1
    return timestamps, values, anomaly_timestamps, anomaly_values


def draw_main_plot(timestamps, values, anomaly_timestamps, anomaly_values):
    fig = go.Figure(
        data=[
            go.Scatter(x=timestamps, y=values[:, 0], line=dict(color='darkblue', width=3), name='L0'),
            go.Scatter(x=timestamps, y=values[:, 1], line=dict(color='blue', width=3), name='L1'),
            go.Scatter(x=timestamps, y=values[:, 2], line=dict(color='blueviolet', width=3), name='L2'),
            go.Scatter(x=timestamps, y=values[:, 3], line=dict(color='darkgreen', width=3), name='R0'),
            go.Scatter(x=timestamps, y=values[:, 4], line=dict(color='green', width=3), name='R1'),
            go.Scatter(x=timestamps, y=values[:, 5], line=dict(color='lime', width=3), name='R2'),
            go.Scatter(
                x=[item for sublist in anomaly_timestamps for item in sublist],
                y=[item for sublist in anomaly_values for item in sublist],
                marker=dict(color="red", size=6),
                mode="markers",
                name="Anomaly",
            )],
        layout=go.Layout(
            height=320,
            xaxis=dict(title='Trace time', nticks=10),  # Limit number of ticks to 10
            yaxis=dict(title='Pressure', range=(0, 1100)),
            template='plotly_white'
        )
    )

    return fig


def draw_sub_plots(timestamps, values, anomaly_timestamps, anomaly_values):
    fig = make_subplots(rows=3, cols=2,
                        subplot_titles=("L0", "R0", "L1", "R1", "L2", "R2"))

    fig.add_trace(go.Scatter(x=timestamps, y=values[:, 0], line=dict(color='darkblue', width=3), name='L0'),
                  row=1, col=1),
    fig.add_trace(go.Scatter(
        x=anomaly_timestamps[0],
        y=anomaly_values[0],
        marker=dict(color="red", size=6),
        mode="markers",
        name="Anomaly",
    ),
        row=1, col=1)
    fig.add_trace(go.Scatter(x=timestamps, y=values[:, 1], line=dict(color='blue', width=3), name='L1'),
                  row=2, col=1)
    fig.add_trace(go.Scatter(
        x=anomaly_timestamps[1],
        y=anomaly_values[1],
        marker=dict(color="red", size=6),
        mode="markers",
        name="Anomaly",
    ),
        row=2, col=1)
    fig.add_trace(go.Scatter(x=timestamps, y=values[:, 2], line=dict(color='blueviolet', width=3), name='L2'),
                  row=3, col=1)
    fig.add_trace(go.Scatter(
        x=anomaly_timestamps[2],
        y=anomaly_values[2],
        marker=dict(color="red", size=6),
        mode="markers",
        name="Anomaly",
    ),
        row=3, col=1)
    fig.add_trace(go.Scatter(x=timestamps, y=values[:, 3], line=dict(color='darkgreen', width=3), name='R0'),
                  row=1, col=2)
    fig.add_trace(go.Scatter(
        x=anomaly_timestamps[3],
        y=anomaly_values[3],
        marker=dict(color="red", size=6),
        mode="markers",
        name="Anomaly",
    ),
        row=1, col=2)
    fig.add_trace(go.Scatter(x=timestamps, y=values[:, 4], line=dict(color='green', width=3), name='R1'),
                  row=2, col=2)
    fig.add_trace(go.Scatter(
        x=anomaly_timestamps[4],
        y=anomaly_values[4],
        marker=dict(color="red", size=6),
        mode="markers",
        name="Anomaly",
    ),
        row=2, col=2)
    fig.add_trace(go.Scatter(x=timestamps, y=values[:, 5], line=dict(color='lime', width=3), name='R2'),
                  row=3, col=2)
    fig.add_trace(go.Scatter(
        x=anomaly_timestamps[5],
        y=anomaly_values[5],
        marker=dict(color="red", size=6),
        mode="markers",
        name="Anomaly",
    ),
        row=3, col=2)

    fig.update_xaxes(nticks=10)
    fig.update_yaxes(range=(0, 1100))
    fig.update_layout(height=420, template='plotly_white', showlegend=False)

    return fig


def draw_histograms(timestamps, values):
    fig = make_subplots(rows=3, cols=2,
                        subplot_titles=("L0", "R0", "L1", "R1", "L2", "R2"))

    fig.add_trace(go.Histogram(x=values[:, 0], marker=dict(color='darkblue'), name='L0'),
                  row=1, col=1),
    fig.add_trace(go.Histogram(x=values[:, 1], marker=dict(color='blue'), name='L1'),
                  row=2, col=1)
    fig.add_trace(go.Histogram(x=values[:, 2], marker=dict(color='blueviolet'), name='L2'),
                  row=3, col=1)
    fig.add_trace(go.Histogram(x=values[:, 3], marker=dict(color='darkgreen'), name='R0'),
                  row=1, col=2)
    fig.add_trace(go.Histogram(x=values[:, 4], marker=dict(color='green'), name='R1'),
                  row=2, col=2)
    fig.add_trace(go.Histogram(x=values[:, 5], marker=dict(color='lime'), name='R2'),
                  row=3, col=2)

    fig.update_xaxes(range=(0, 1100))
    fig.update_layout(height=420, template='plotly_white', showlegend=False)

    return fig


def draw_feet_plot(values):
    fig = go.Figure(
        data=[
            go.Scatter(x=[0.35], y=[0.7], marker=dict(color='darkblue', size=values[0]/50), name='L0'),
            go.Scatter(x=[0.35], y=[0.7], opacity=0.2, marker=dict(color='darkblue', size=20), name='L0'),
            go.Scatter(x=[0.15], y=[0.55], marker=dict(color='blue', size=values[1]/50), name='L1'),
            go.Scatter(x=[0.15], y=[0.55], opacity=0.2, marker=dict(color='blue', size=20), name='L1'),
            go.Scatter(x=[0.28], y=[0.12], marker=dict(color='blueviolet', size=values[2]/50), name='L2'),
            go.Scatter(x=[0.28], y=[0.12], opacity=0.2, marker=dict(color='blueviolet', size=20), name='L2'),
            go.Scatter(x=[0.65], y=[0.7], marker=dict(color='darkgreen', size=values[3]/50), name='R0'),
            go.Scatter(x=[0.65], y=[0.7], opacity=0.2, marker=dict(color='darkgreen', size=20), name='R0'),
            go.Scatter(x=[0.85], y=[0.55], marker=dict(color='green', size=values[4]/50), name='R1'),
            go.Scatter(x=[0.85], y=[0.55], opacity=0.2, marker=dict(color='green', size=20), name='R1'),
            go.Scatter(x=[0.72], y=[0.12], marker=dict(color='lime', size=values[5]/50), name='R2'),
            go.Scatter(x=[0.72], y=[0.12], opacity=0.2, marker=dict(color='lime', size=20), name='R2'),
            ],
        layout=go.Layout(
            xaxis=dict(range=(0, 1), showgrid=False, zeroline=False, visible=False),
            yaxis=dict(range=(0, 1), showgrid=False, zeroline=False, visible=False),
            width=420,
            height=420,
            template='plotly_white',
            showlegend=False
        )
    )

    fig.add_layout_image(
        dict(
            source="https://raw.githubusercontent.com/wikturzz/ppdv-projekt/master/img/feet.jpg",
            x=0,
            y=1,
            sizex=1,
            sizey=1,
            sizing="stretch",
            opacity=0.8,
            layer="below")
    )

    return fig


app = dash.Dash(__name__)

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    html.H1(id='H1', children='PPDV Project - Jakub Miętki & Wiktor Zaremba',
            style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),

    html.Div(id='content', children=[
    ])
])


def create_layout(_patient_id):
    global patient_id
    patient_id = _patient_id
    patient_data = get_storage()[patient_id]

    if patient_data["disabled"]:
        disabled = "Yes"
    else:
        disabled = "No"

    d = {
        'Firstname': [patient_data["firstname"]],
        'Lastname': [patient_data["lastname"]],
        'Birthdate': [patient_data["birthdate"]],
        'Disabled': [disabled],
        'Trace name:': [patient_data["name"]]
    }

    df = pd.DataFrame(data=d)
    timestamps, values, anomaly_timestamps, anomaly_values = get_data()

    return html.Div(id='content-container', children=[
        dcc.Dropdown(
            id='patient-dropdown',
            options=[
                {'label': 'Patient 1', 'value': 1},
                {'label': 'Patient 2', 'value': 2},
                {'label': 'Patient 3', 'value': 3},
                {'label': 'Patient 4', 'value': 4},
                {'label': 'Patient 5', 'value': 5}
            ],
            value=patient_id
        ),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[
                {'id': c, 'name': c}
                for c in df.columns
            ],
        ),
        html.Center(children=[
            dcc.Graph(id='feet_plot', figure=draw_feet_plot(values[len(values) - 1]))
        ]
        ),
        dcc.Graph(id='the_main_plot', figure=draw_main_plot(timestamps, values, anomaly_timestamps, anomaly_values)),
        dcc.Graph(id='the_sub_plots', figure=draw_sub_plots(timestamps, values, anomaly_timestamps, anomaly_values)),
        dcc.Graph(id='the_histograms', figure=draw_histograms(timestamps, values)),
        dcc.Interval(id='interval', interval=1000, n_intervals=0)
    ])


@app.callback(Output('content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if len(pathname) == 10 and pathname[0:9] == '/patient/' and int(pathname[9]) in range(1, 6):
        return create_layout(int(pathname[9]))
    else:
        return create_layout(1)


@app.callback(Output(component_id='the_main_plot', component_property='figure'),
              Output(component_id='the_sub_plots', component_property='figure'),
              Output(component_id='the_histograms', component_property='figure'),
              Output(component_id='feet_plot', component_property='figure'),
              [Input(component_id='interval', component_property='n_intervals')])
def graph_update(n_intervals):
    timestamps, values, anomaly_timestamps, anomaly_values = get_data()
    return draw_main_plot(timestamps, values, anomaly_timestamps, anomaly_values), \
           draw_sub_plots(timestamps, values, anomaly_timestamps, anomaly_values), \
           draw_histograms(timestamps, values), \
           draw_feet_plot(values[len(values) - 1])


@app.callback(Output(component_id='url', component_property='pathname'),
              [Input(component_id='patient-dropdown', component_property='value')])
def dropdown_update(value):
    return f'/patient/{value}'
