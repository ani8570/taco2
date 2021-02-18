from librosa.core.spectrum import stft
from numpy import lib
from tqdm import tqdm
import numpy as np
import os, glob, re, librosa, argparse,json
import pandas as pd
from util.text import text_to_sequence
from util.hparams import *


def make_folder(out_dir) :
    """
    making folder at out_dir

    arg : 
        dir : folder dir
    """
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir,"text"),   exist_ok=True)
    os.makedirs(os.path.join(out_dir,"mel"),    exist_ok=True)
    os.makedirs(os.path.join(out_dir,"dec"),    exist_ok=True)
    os.makedirs(os.path.join(out_dir,"spec"),   exist_ok=True)

def load_data(dataset_dir) :
    """
    Get key, value in json file 
    
    arg : 
        dir : folder dir
    """
    text_dir = glob.glob(os.path.join(dataset_dir, '*.json'))
    keyL = []
    valueL = []
    with open(text_dir[0],encoding='utf-8') as f:
        content = f.read()
        data = json.loads(content)
        for key, text in data.items():
            keyL.append(key)
            valueL.append(text)
    return keyL, valueL

def make_text(text, out_dir):
    # text
    print('Load text')
    filters = '([.,!?])'
    text_len = []
    for idx, s in enumerate(tqdm(text)):
        sentense = re.sub(re.compile(filters), '' ,s)
        sentense = text_to_sequence(sentense)
        text_len.append(len(sentense))
        text_name = 'kss-text-%05d.npy' %idx
        np.save(os.path.join(out_dir, "text", text_name), sentense, allow_pickle=False)
    np.save(os.path.join(out_dir, "text_len.npy"), np.array(text_len))
    print("Text done")

def make_wav(wav_dir, out_dir):
    print('Load audio')
    mel_len_list = []
    for idx, fn in enumerate(tqdm(wav_dir)):
        file_dir = './kss/' + fn
        wav, _ = librosa.load(file_dir, sr=sample_rate)
        wav, _ = librosa.effects.trim(wav)
        wav = np.append(wav[0], wav[1:] - preemphasis * wav[:-1])
        stft = librosa.stft(wav, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
        stft = np.abs(stft)
        mel_filter = librosa.filters.mel(sample_rate, n_fft, mel_dim)
        mel_spec = np.dot(mel_filter, stft)

        mel_spec = 20 * np.log10(np.maximum(1e-5, mel_spec))
        stft = 20 * np.log(np.maximum(1e-5, mel_spec))

        mel_spec = np.clip((mel_spec - ref_db + max_db) / max_db, 1e-8, 1)
        stft = np.clip((stft - ref_db + max_db) / max_db, 1e-8, 1)

        mel_spec = mel_spec.T.astype(np.float32)
        stft = stft.T.astype(np.float32)
        mel_len_list.append([mel_spec.shape[0], idx])

        # padding
        remainder = mel_spec.shape[0] % reduction
        if remainder != 0:
            mel_spec = np.pad(mel_spec, [[0, reduction - remainder], [0,0]], mode='constant')
            stft = np.pad(stft, [[0, reduction - remainder], [0,0]], mode='constant')

        mel_name = 'kss-mel-%05d.npy' %idx
        np.save(os.path.join(out_dir+'/mel',mel_name), mel_spec, allow_pickle=False)

        stft_name = 'kss-mel-%05d.npy' %idx
        np.save(os.path.join(out_dir+'/mel',stft_name), stft, allow_pickle=False)

        # Decoder Input
        mel_spec = mel_spec.reshape((-1, mel_dim * reduction))
        dec_input = dec_input[: -mel_dim:]
        dec_name = 'kss-dec-%05d.npy' %idx
        np.save(os.path.join(out_dir+'/dec',dec_name), dec_input, allow_pickle=False)

    melspectrogram
    mel_len = sorted(mel_len_list)


def main() :
    parser = argparse.ArgumentParser()
    
    parser.add_argument ('--log_dir', default='/kss')
    parser.add_argument ('--out_dir', default='./data')
    config = parser.parse_args()
    log_dir = './dataset' + config.log_dir
    out_dir = config.out_dir

    make_folder(out_dir=out_dir)
    wav_dir, text = load_data(log_dir)
    make_text(text=text, out_dir=out_dir)
    make_wav(wav_dir=wav_dir, out_dir=out_dir)


if __name__ == '__main__':
    main()