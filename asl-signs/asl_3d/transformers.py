import pandas as pd

def create_landmark_lines(frame_landmarks, landmarks_type):
    empty_row = pd.Series({
        'frame': None, 'row_id': None, 'type': None, 'x': None, 'y': None, 'z': None
    })
    frame_landmarks = (frame_landmarks.loc[:, ['landmark_index', 'frame', 'row_id', 'type', 'x', 'y', 'z']]
                       .set_index('landmark_index'))
    
    if frame_landmarks.empty:
        line_indices = [None]
    elif landmarks_type in ['hand', 'left_hand', 'right_hand']:
        line_indices = [0, 1, None, 0, 5, None, 0, 17, None, 
                        1, 2, 3, 4, None,
                        5, 6, 7, 8, None,
                        5, 9, None,
                        9, 10, 11, 12, None,
                        9, 13, None,
                        13, 14, 15, 16, None,
                        13, 17, None,
                        17, 18, 19, 20, None
                       ]
    elif landmarks_type == "pose":
        line_indices = [0, 1, 2, 3, 7, None, 
                        0, 4, 5, 6, 7, 8, None,
                        11, 13, 15, 17, 19, 15, 21, None,
                        11, 12, 14, 16, 18, 20, 16, 22, None,
                        11, 23, 25, 27, 31, 29, 27, None,
                        12, 24, 26, 28, 30, 32, 28, None,
                        23, 24, None
               ]
    else:
        raise ValueError()
    lines = pd.DataFrame([frame_landmarks.loc[i, ] if i is not None else empty_row
                          for i in line_indices
                         ])
    return lines