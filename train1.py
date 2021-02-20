from util.hparams import *
import glob, os, random
import numpy as np

data_dir = './data/kss'
text_list = glob.glob(os.path.join(data_dir + '/text', '*.npy'))
mel_list = glob.glob(os.path.join(data_dir + '/mel', '*.npy'))
dec_list = glob.glob(os.path.join(data_dir + '/dec', '*.npy'))

fn = os.path.join(data_dir + '/mel_len.npy')
if not os.path.isfile(fn):
    mel_len_list = []
    for i in range(len(mel_list)):
        mel_length = np.load(mel_list[i]).shape[0]
        mel_len_list.append([mel_length,i])
    
    mel_len = sorted(mel_len_list)
    np.save(os.path.join(data_dir + '/mel_len.npy'), np.array(mel_len))

text_len = np.load(os.path.join(data_dir + '/text_len.npy'))
mel_len = np.load(os.path.join(data_dir + '/mel_len.npy'))

def DataGenerator():
    while True:
        #  왜?
        idx_list = np.random.choice(len(mel_list), batch_size * batch_size)
        idx_list = list(idx_list)
        idx_list = [idx_list[i:i+batch_size] for i in range(0, len(idx_list), batch_size)]
        random.shuffle(idx_list)
        print(1)


def main():
    DataGenerator()

if __name__=="__main__":
    main()