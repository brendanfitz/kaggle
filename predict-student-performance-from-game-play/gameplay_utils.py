from pathlib import Path
import numpy as np
import os

iskaggle = os.environ.get('KAGGLE_KERNEL_RUN_TYPE', '')
if iskaggle:
    data_wd = Path('..') / 'input'  / 'competition'
else:
    data_wd = Path.home() / '.data' / 'predict-student-performance-from-game-play'

dtypes = dict(
    elapsed_time=np.int32, event_name='category', name='category', level=np.uint8, 
    room_coor_x=np.float32, room_coor_y=np.float32, screen_coor_x=np.float32,
    screen_coor_y=np.float32, hover_duration=np.float32, text='category',
    fqid='category', room_fqid='category', text_fqid='category',
    fullscreen='category', hq='category', music='category', level_group='category'
)

level_group_kwargs = dict(categories=["0-4", "5-12", "13-22"], ordered=True)