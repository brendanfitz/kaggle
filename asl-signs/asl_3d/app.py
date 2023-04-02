import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from extractors import LandmarkSequence
from transformers import create_landmark_lines
from visualizers import create_traces, CAMERAS
import plotly.express as px

GRAPH_SIZE = 750
LM_TYPES = ['left_hand', 'pose', 'right_hand']

seq = LandmarkSequence('1000210073')


figures = {
    lm_type: go.Figure(data=create_traces(seq, lm_type), layout=go.Layout(title=lm_type))
    for lm_type in LM_TYPES
}

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1('Landmark Sequences', style=dict(textAlign='center')),
    html.Div(
        id='graphs',
        children=[dcc.Graph(id=lm_type, figure=figures[lm_type], style=dict(width='30%', display='inline-block'))
                  for lm_type in LM_TYPES],
        style=dict(style='display:flex; flex-direction: row; justify-content: center; align-items: center')
    ),
    dcc.Slider(
        id='frame-picker',
        min=min(seq.frames),
        max=max(seq.frames),
        step=None,
        marks={frame: str(frame) for frame in seq.frames},
        value=min(seq.frames)
    )
])

@app.callback(Output('pose', 'figure'), [Input('frame-picker', 'value')])
def update_figure(selected_frame):
    traces = figures['pose'].data
    for i, frame in enumerate(seq.frames):
        traces[i].visible = frame == selected_frame
    
    fig = go.Figure(dict(data=traces))
    fig.update_layout(
        scene_camera=CAMERAS['pose'],
        height=GRAPH_SIZE, width=GRAPH_SIZE,
        title='pose',
    )
    return fig

@app.callback(Output('left_hand', 'figure'), [Input('frame-picker', 'value')])
def update_figure_lh(selected_frame):
    traces = figures['left_hand'].data
    for i, frame in enumerate(seq.frames):
        traces[i].visible = frame == selected_frame
    
    fig = go.Figure(dict(data=traces), figures['left_hand'].layout)
    fig.update_layout(
        scene_camera=CAMERAS['left_hand'],
        height=GRAPH_SIZE, width=GRAPH_SIZE,
        title='Left Hand'
    )
    return fig
        
@app.callback(Output('right_hand', 'figure'), [Input('frame-picker', 'value')])
def update_figure_lh(selected_frame):
    traces = figures['right_hand'].data
    for i, frame in enumerate(seq.frames):
        traces[i].visible = frame == selected_frame
    
    fig = go.Figure(dict(data=traces), figures['right_hand'].layout)
    fig.update_layout(
        scene_camera=CAMERAS['right_hand'],
        height=GRAPH_SIZE, width=GRAPH_SIZE,
        title='Right Hand'
    )
    return fig
        

if __name__ == '__main__':
    app.run_server(debug=True)