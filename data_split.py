import pathlib
import os
from tqdm import tqdm
import pandas


def data_split(path, num_files):
    csv_file = pandas.read_csv('/Volumes/Ext_SSD/e-gmd-v1.0.0/e-gmd-v1.0.0.csv')
    sum_agree = 0  # sum to check

    test_files = []
    train_files = []
    val_files = []

    for file in tqdm(path, total=num_files, desc="Checking For Test/Train/Val -->"):
        copy_path = file
        file = str(file)  # convert path to string
        file = file[30:]  # drop part before 'drummer...', must be adjusted to your specific path

        if 'midi' in file:
            ind = csv_file[csv_file['midi_filename'] == file].index.values  # get index where file name is identical
            x = list(csv_file.loc[ind, 'split'])  # get test/train/validation string connected to specific file
        elif 'wav' in file:
            ind = csv_file[csv_file['audio_filename'] == file].index.values  # get index where file name is identical
            x = list(csv_file.loc[ind, 'split'])  # get test/train/validation string connected to specific file

        if x[0] == 'test':
            test_files.append(copy_path)
        elif x[0] == 'train':
            train_files.append(copy_path)
        elif x[0] == 'validation':
            val_files.append(copy_path)
        else:
            print('---> other ', x[0])

        sum_agree += 1

    print(num_files, sum_agree)

    for i in tqdm(test_files, total=len(test_files), desc="Moving test files -->"):
        i = str(i)
        filename = i[30:].replace('/', '-')
        os.rename(i, f'/Volumes/Ext_SSD/e-gmd-v1.0.0/Test/{filename}')
    print(f"Done copying {len(test_files)} test files")

    for n in tqdm(train_files, total=len(train_files), desc="Moving train files -->"):
        n = str(n)
        filename = n[30:].replace('/', '-')
        os.rename(n, f'/Volumes/Ext_SSD/e-gmd-v1.0.0/Train/{filename}')
    print(f"Done copying {len(train_files)} train files")

    for k in tqdm(val_files, total=len(val_files), desc="Moving val files -->"):
        k = str(k)
        filename = k[30:].replace('/', '-')
        os.rename(k, f'/Volumes/Ext_SSD/e-gmd-v1.0.0/Val/{filename}')
    print(f"Done copying {len(val_files)} val files")

    print(sum_agree == num_files)  # check if number of copied files is equal the number of existing files


if __name__ == '__main__':
    # calculate the number of wav files
    path_wav = pathlib.Path('/Volumes/Ext_SSD/e-gmd-v1.0.0').glob('**/*.wav')
    sum_wav = 0
    for wav in path_wav:
        sum_wav += 1
    print(f'Number of .wav files {sum_wav}')

    # put files into designated folders: test/train/validation
    path_wav = pathlib.Path('/Volumes/Ext_SSD/e-gmd-v1.0.0').glob('**/*.wav')
    data_split(path_wav, sum_wav)

    # calculate the number of midi files
    path_midi = pathlib.Path('/Volumes/Ext_SSD/e-gmd-v1.0.0').glob('**/*.midi')
    sum_midi = 0
    for midi in path_midi:
        sum_midi += 1
    print(f'Number of .midi files {sum_midi}')

    # put files into designated folders: test/train/validation
    path_midi = pathlib.Path('/Volumes/Ext_SSD/e-gmd-v1.0.0').glob('**/*.midi')
    data_split(path_midi, sum_midi)