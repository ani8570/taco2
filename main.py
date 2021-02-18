from librosa.core.spectrum import stft
from numpy import lib
from pandas.io import json
from tqdm import tqdm
import numpy as np
import os, glob, re, librosa, argparse
import pandas as pd
from util.text import text_to_sequence
from util.hparams import *

def make_folder(log_dir, out_dir) :
    text_dir = glob.glob(os.path.join(log_dir, '*.json'))
    filter = "([.,!?])"
    print(text_dir)
    with open("C:\\github.com\\ani8570\\taco2\\dataset\\kss\\kss.json", "r", encoding="utf-8") as json_file:
        print(json_file)
        
    # wav_dir = metadata[0].values
    # text = metadata[3].values

    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir,"text"),   exist_ok=True)
    os.makedirs(os.path.join(out_dir,"mel"),    exist_ok=True)
    os.makedirs(os.path.join(out_dir,"dec"),    exist_ok=True)
    os.makedirs(os.path.join(out_dir,"spec"),   exist_ok=True)
    return wav_dir, text



def make_text(text, out_dir):
    # text
    print('Load text')
    filters = '([.,!?])'
    text_len = []
    for idx, s in enumerate(tqdm(text)):
        sentense = re.sub(re.compile(filter), '' ,s)
        sentense = text_to_sequence(sentense)
        text_len.append(len(sentense))
        text_name = 'kss-text-%05d.npy' %idx
        np.save(os.path.join(out_dir, "text", text_name), sentense, allow_pickle=False)
    np.save(os.path.join(out_dir, "text_len.npy"), np.array(text_len))
    print("Text done")

# print('Load audio')
# mel_len_list = []
# for idx, fn in enumerate(tqdm(wav_dir)):
#     file_dir = './kss/' + fn
#     wav, _ = librosa.load(file_dir, sr=sample_rate)
#     wav, _ = librosa.effects.trim(wav)
#     wav = np.append(wav[0], wav[1:] - preemphasis * wav[:-1])
#     stft = librosa.stft(wav, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
#     stft = np.abs(stft)
#     mel_filter = librosa.filters.mel(sample_rate, n_fft, mel_dim)
#     mel_spec = np.dot(mel_filter, stft)

#     mel_spec = 20 * np.log10(np.maximum(1e-5, mel_spec))
#     stft = 20 * np.log(np.maximum(1e-5, mel_spec))

#     mel_spec = np.clip((mel_spec - ref_db + max_db) / max_db, 1e-8, 1)
#     stft = np.clip((stft - ref_db + max_db) / max_db, 1e-8, 1)

#     mel_spec = mel_spec.T.astype(np.float32)
#     stft = stft.T.astype(np.float32)
#     mel_len_list.append([mel_spec.shape[0], idx])

#     # padding
#     remainder = mel_spec.shape[0] % reduction
#     if remainder != 0:
#         mel_spec = np.pad(mel_spec, [[0, reduction - remainder], [0,0]], mode='constant')
#         stft = np.pad(stft, [[0, reduction - remainder], [0,0]], mode='constant')
    
#     mel_name = 'kss'

def main() :
    parser = argparse.ArgumentParser()
    parser.add_argument ('--log_dir', default='./dataset\\kss')
    parser.add_argument ('--out_dir', default='./data')
    config = parser.parse_args()
    log_dir = config.log_dir
    out_dir = config.out_dir
    make_folder(log_dir=log_dir, out_dir=out_dir)



if __name__ == '__main__':
    main()