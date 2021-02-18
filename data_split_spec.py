import pathlib
import pylab
import shutil, os
import numpy as np
import librosa
from librosa import display
from tqdm import tqdm  # progress bar
import pandas


def spectrogram_image(plt_type, filepath):
    # convert path back to string
    filepath = str(filepath)

    # replace / for image path
    sav_str = filepath.replace('/', '-')

    # set image path
    img = f'/Volumes/Ext_SSD/e-gmd-v1.0.0/{plt_type}/{plt_type}-{sav_str[30:]}.jpg'

    # plot some audio waveforms
    audio, sr = librosa.core.load(filepath, sr=None)

    # calculate stft
    stft = librosa.stft(audio, n_fft=2048, hop_length=256, win_length=2048)

    pylab.axis('off')  # no axis
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge

    # save as np.array/ hop length, tensorflow records
    if plt_type == 'Mel':
        # calculate melspec
        melspec = librosa.feature.melspectrogram(audio, n_fft=2048, hop_length=256, win_length=2048, n_mels=64,
                                                 fmax=int(sr / 2))
        melspec = librosa.amplitude_to_db(melspec, ref=np.max)  # not db but log 10e-6 add
        # print(melspec.shape) bins and frames
        # plot
        librosa.display.specshow(melspec, x_axis='time', y_axis='mel', sr=sr, hop_length=256)
        # save image
        pylab.savefig(img, bbox_inches=None, pad_inches=0)
        pylab.close()

    elif plt_type == 'Mag':
        # calculate magnitude and scale to dB
        magspec = librosa.amplitude_to_db(np.abs(stft), ref=np.max)
        # plot
        librosa.display.specshow(magspec, x_axis='time', y_axis='linear', sr=sr, hop_length=256)
        # save image
        pylab.savefig(img, bbox_inches=None, pad_inches=0)
        pylab.close()

    else:
        print("Input must be Mel or Mag.")


def data_split(path, num_files):
    csv_file = pandas.read_csv('/Volumes/Ext_SSD/e-gmd-v1.0.0/e-gmd-v1.0.0.csv')
    sum_agree = 0  # sum to check

    test_files = []
    train_files = []
    val_files = []

    '''for wav in path:
        print(wav)'''

    for file in tqdm(path, total=num_files, desc="Checking For Test/Train/Val -->"):
        copy_path = file
        file = str(file)  # convert path to string
        file = file[30:]  # drop part before 'drummer...'

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


    # path to all wav files
    # path_wav[:1000] check metrics

    # iterate over every wav file path
    '''for file in tqdm(path_wav, total=sum_wav, desc="Progress -->"):
        spectrogram_image('Mel', file)
        spectrogram_image('Mag', file)
    '''

    print('End')
