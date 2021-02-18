import glob, os, json
import pandas as pd

def main():
    log_dir = './dataset/kss/'
    text_dir = glob.glob(os.path.join(log_dir, '*.txt'))
    
    metadata = pd.read_csv(text_dir[0], dtype='object', sep='|', header=None)
    wav_dir = metadata[0].values
    text = metadata[3].values
    file_data = {}
    for i in range(len(wav_dir)):
        s = log_dir + wav_dir[i]
        file_data[s] = text[i]
    with open(log_dir+"kss.json", "w", encoding="utf-8") as fp:
        json.dump(file_data, fp, ensure_ascii=False, indent="\t")  
    fp.close()

if __name__=='__main__':
    main()