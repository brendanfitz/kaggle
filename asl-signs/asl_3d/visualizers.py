import plotly.graph_objects as go
from transformers import create_landmark_lines

def create_traces(seq, lm_type):
    mask = seq.landmarks.type == lm_type
    landmarks = seq.landmarks.loc[mask, ]
    traces = list()
    for frame in seq.frames:
        mask = landmarks.frame == frame
        frame_landmarks = landmarks.loc[mask, ]
        landmark_lines = create_landmark_lines(frame_landmarks, lm_type)
        traces.append(go.Scatter3d(
            x=landmark_lines.x, y=landmark_lines.y, z=landmark_lines.z,
            mode="markers+lines", visible=False, name=str(frame)
        ))
    return traces



CAMERAS = dict(
    pose=dict(
        up=dict(x=0, y=-1, z=0),
        eye=dict(x=0, y=0, z=-2.5)
    ),
    left_hand=dict(
        up=dict(x=-0.5, y=-1, z=-0.5),
        eye=dict(x=-1.5, y=1, z=-2.5)
    ),
    right_hand=dict(
        up=dict(x=-0.5, y=-1, z=-0.5),
        eye=dict(x=-1.5, y=1, z=-2.5)
    ),
)