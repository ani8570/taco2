from tqdm import tqdm
import numpy as np
import os, glob, re
import pandas as pd
from util.text import text_to_sequence

text_dir = glob.glob(os.path.join('./kss', '*.txt'))
filter = "([.,!?])"

metadata = pd.read_csv(text_dir[0], dtype='object', sep='|', header=None)
print(os.path.join('./kss', '*.txt'))
wav_dir = metadata[0].values
text = metadata[3].values

out_dir = './data'
os.makedirs(out_dir, exist_ok=True)
os.makedirs(os.path.join(out_dir,"text"),   exist_ok=True)
os.makedirs(os.path.join(out_dir,"mel"),    exist_ok=True)
os.makedirs(os.path.join(out_dir,"dec"),    exist_ok=True)
os.makedirs(os.path.join(out_dir,"spec"),   exist_ok=True)

#text
print('Load text')
text_len = []
for idx, s in enumerate(tqdm(text)):
    sentense = re.sub(re.compile(filter), '' ,s)
    sentense = text_to_sequence(sentense)
    text_len.append(len(sentense))
    text_name = 'kss-text-%05d.npy' %idx
    np.save(os.path.join(out_dir, "text", text_name), sentense, allow_pickle=False)