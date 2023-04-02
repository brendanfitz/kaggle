import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from extractors import LandmarkSequence
from transformers import create_landmark_lines
from visualizers import create_traces, change_visible_frame
import plotly.express as px

LM_TYPES = ['right_hand', 'pose', 'left_hand']

seq = LandmarkSequence('1002052130')

graph_style = dict(width='30%', display='inline-block')

sign = 'TV'
sequences = seq.SIGN_META.loc[seq.SIGN_META.sign == sign, ].index.tolist()

figures = {
    lm_type: go.Figure(data=create_traces(seq, lm_type), layout=go.Layout(title=lm_type))
    for lm_type in LM_TYPES
}

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1('Landmark Sequences', style=dict(textAlign='center')),
    html.Div(
        id='sequence-selectors',
        children=[
            dcc.Dropdown(
                id='sign-selector',
                options=seq.SIGN_META.sign.unique(),
                value=sign,
            ),
            dcc.Dropdown(
                id='sequence-selector',
                options=sequences,
                value=sequences[0],
            )
        ]
    ),
    html.Div(
        id='graphs',
        children=[dcc.Graph(id=lm_type, figure=figures[lm_type], style=dict(width='30%', display='inline-block'))
                  for lm_type in LM_TYPES],
        style=dict(style='display:flex; flex-direction: row; justify-content: center; align-items: center')
    ),
    html.Div(
        id='frame-div',
        children=[
            dcc.Slider(
                id='frame-picker',
                min=min(seq.frames),
                max=max(seq.frames),
                step=None,
                marks={frame: str(frame) for frame in seq.frames},
                value=min(seq.frames)
            )
        ]

    )
])

@app.callback(Output('pose', 'figure'), [Input('frame-picker', 'value')])
def update_pose(selected_frame):
    lm_type = 'pose'
    fig = change_visible_frame(lm_type, figures[lm_type], seq.frames, selected_frame)
    return fig

@app.callback(Output('left_hand', 'figure'), [Input('frame-picker', 'value')])
def update_left_hand(selected_frame):
    lm_type = 'left_hand'
    fig = change_visible_frame(lm_type, figures[lm_type], seq.frames, selected_frame)
    return fig
        
@app.callback(Output('right_hand', 'figure'), [Input('frame-picker', 'value')])
def update_right_hand(selected_frame):
    lm_type = 'right_hand'
    fig = change_visible_frame(lm_type, figures[lm_type], seq.frames, selected_frame)
    return fig

@app.callback(Output('sequence-selector', 'options'), [Input('sign-selector', 'value')])
def update_sequence_options(sign):
    sequences = seq.SIGN_META.loc[seq.SIGN_META.sign == sign, ].index.tolist()
    return sequences

@app.callback(Output('graphs', 'children'), [Input('sequence-selector', 'value')])
def update_figs(sequence_id):
    global seq
    global figures
    seq = LandmarkSequence(sequence_id)
    figures = {
        lm_type: go.Figure(data=create_traces(seq, lm_type), layout=go.Layout(title=lm_type))
        for lm_type in LM_TYPES
    }
    children=[dcc.Graph(id=lm_type, figure=figures[lm_type], style=graph_style)
              for lm_type in LM_TYPES]
    return children

@app.callback(Output('frame-div', 'children'), [Input('graphs', 'children')])
def update_frames(_):
    return dcc.Slider(
        id='frame-picker',
        min=min(seq.frames),
        max=max(seq.frames),
        step=None,
        marks={frame: str(frame) for frame in seq.frames},
        value=min(seq.frames)
    )

    
        

if __name__ == '__main__':
    app.run_server(debug=True)