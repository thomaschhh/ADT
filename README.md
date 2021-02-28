# Automatic Drum Transcription

This project was done in the winter semester of 2020 as part of the class *Deep Learning for Audio Event Detection* at TU Berlin.

We used [https://magenta.tensorflow.org/datasets/e-gmd#download](https://magenta.tensorflow.org/datasets/e-gmd#download) as our training and testing dataset. If you want to split the dataset into Test / Train / Val splits, use the following file: [data_split.py](data_split.py). 

After the preprocessing, the data is stored in TFRecords. In our case, we weren't able to train the models on a GPU which is why we only trained them for 20 epochs. 
