import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from extractors import LandmarkSequence
from transformers import create_landmark_lines
from visualizers import create_traces, change_visible_frame
import plotly.express as px

LM_TYPES = ['right_hand', 'pose', 'left_hand']

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
    lm_type = 'pose'
    fig = change_visible_frame(lm_type, figures[lm_type], seq.frames, selected_frame)
    return fig

@app.callback(Output('left_hand', 'figure'), [Input('frame-picker', 'value')])
def update_figure_lh(selected_frame):
    lm_type = 'left_hand'
    fig = change_visible_frame(lm_type, figures[lm_type], seq.frames, selected_frame)
    return fig
        
@app.callback(Output('right_hand', 'figure'), [Input('frame-picker', 'value')])
def update_figure_lh(selected_frame):
    lm_type = 'right_hand'
    fig = change_visible_frame(lm_type, figures[lm_type], seq.frames, selected_frame)
    return fig
        

if __name__ == '__main__':
    app.run_server(debug=True)