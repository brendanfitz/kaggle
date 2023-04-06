import pandas as pd
from pathlib import Path
from transformers import interpolate_values

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
    
    def __init__(self, sequence_id, interpolate=False):
        self.sequence_id = sequence_id
        self.interpolate = interpolate

        self.meta = self.SIGN_META.loc[self.sequence_id, :]
        self.landmarks = self.read_parquet(self.meta['path'])
        if interpolate:
            self.landmarks = interpolate_values(self.landmarks)
        
        self.frames = self.landmarks.frame.unique().tolist()
    
    def read_parquet(self, pq_name):
        landmarks = pd.read_parquet(path / pq_name)
        landmarks = landmarks.loc[landmarks.type.isin(self.LANDMARK_TYPES), ]
        return landmarks