import pandas as pd
from pathlib import Path

path = Path.home() / '.data' / 'asl-signs'

def fetch_sign_meta():
    sign_meta = (pd.read_csv(path / 'train_with_meta.csv', dtype=dict(sequence_id=str))
                 .set_index('sequence_id')
                )
    return sign_meta

class LandmarkSequence:
    COORD_COLS = ['x', 'y', 'z']
    LANDMARK_TYPES = ['left_hand', 'pose', 'right_hand']
    SIGN_META = fetch_sign_meta()
    
    def __init__(self, sequence_id):
        self.sequence_id = sequence_id
        self.meta = self.SIGN_META.loc[self.sequence_id, :]
        self.landmarks = self.read_parquet(self.meta['path'])
        self.frames = self.landmarks.frame.unique().tolist()
    
    def read_parquet(self, pq_name):
        landmarks = pd.read_parquet(path / pq_name)
        landmarks = landmarks.loc[landmarks.type.isin(self.LANDMARK_TYPES), ]
        pose_mask = landmarks.loc[:, 'type'] == 'pose'
        landmarks.loc[pose_mask, 'x'] = -landmarks.loc[pose_mask, 'x']
        return landmarks