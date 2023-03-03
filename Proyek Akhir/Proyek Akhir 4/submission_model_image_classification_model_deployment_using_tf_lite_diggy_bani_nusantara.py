# -*- coding: utf-8 -*-
"""Submission Model Image Classification Model Deployment using TF-Lite - Diggy Bani Nusantara.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VjCw8RX7zXxBn3Z0HjOxJ4VfxA2GlroF

Nama : Diggy Bani Nusantara; Kelas : Belajar Machine Learning Untuk Pemula; No. Registrasi : 1494037162101-336; Program : FGA; Model Fruit Image Classification Model Deployment using TF-Lite;
"""

# Commented out IPython magic to ensure Python compatibility.
#Library
import zipfile
import os
import glob 
import warnings

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Activation, Dense, Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam
import tensorflow as tf

from keras.preprocessing import image
import keras.utils as image
from google.colab import files
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline

#Dataset
!pip install -q Kaggle

uploaded = files.upload()

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!kaggle datasets download -d sshikamaru/fruit-recognition

#Extract
extract_zip = 'fruit-recognition.zip'
out_zip = zipfile.ZipFile(extract_zip, 'r')
out_zip.extractall('/content/datasets')
out_zip.close()

#Location
dir_dataset = "/content/datasets/train/train"
dir_mango = os.path.join("/content/datasets/train/train/Mango")
dir_orange = os.path.join("/content/datasets/train/train/Orange")
dir_pear = os.path.join("/content/datasets/train/train/Pear")

#Jumlah Data
total_image = len(list(glob.iglob("/content/datasets/train/train/*/*.*", recursive=True)))
print("Total Data Image JPEG     : ",total_image)

total_mango = len(os.listdir(dir_mango))
total_orange = len(os.listdir(dir_orange))
total_pear = len(os.listdir(dir_pear))

print("Total Data Mango Image    : ",total_mango)
print("Total Data Orange Image   : ",total_orange)
print("Total Data Pear Image     : ",total_pear)

#Delete Unused Datasets
!rm -rf /content/datasets/train/train/'Apple Braeburn'
!rm -rf /content/datasets/train/train/'Apple Granny Smith'
!rm -rf /content/datasets/train/train/Apricot
!rm -rf /content/datasets/train/train/Avocado
!rm -rf /content/datasets/train/train/Banana
!rm -rf /content/datasets/train/train/Blueberry
!rm -rf /content/datasets/train/train/'Cactus fruit'
!rm -rf /content/datasets/train/train/Cantaloupe
!rm -rf /content/datasets/train/train/Cherry
!rm -rf /content/datasets/train/train/Clementine
!rm -rf /content/datasets/train/train/Corn
!rm -rf /content/datasets/train/train/'Cucumber Ripe'
!rm -rf /content/datasets/train/train/'Grape Blue'
!rm -rf /content/datasets/train/train/Kiwi
!rm -rf /content/datasets/train/train/Lemon
!rm -rf /content/datasets/train/train/Limes
!rm -rf /content/datasets/train/train/'Onion White'
!rm -rf /content/datasets/train/train/Papaya
!rm -rf /content/datasets/train/train/'Passion Fruit'
!rm -rf /content/datasets/train/train/Peach
!rm -rf /content/datasets/train/train/'Pepper Green'
!rm -rf /content/datasets/train/train/'Pepper Red'
!rm -rf /content/datasets/train/train/Pineapple
!rm -rf /content/datasets/train/train/Plum
!rm -rf /content/datasets/train/train/Pomegranate
!rm -rf /content/datasets/train/train/'Potato Red'
!rm -rf /content/datasets/train/train/Raspberry
!rm -rf /content/datasets/train/train/Strawberry
!rm -rf /content/datasets/train/train/Tomato
!rm -rf /content/datasets/train/train/Watermelon
!ls /content/datasets/train/train/

#Validation 20%
val_size = 0.2

train_datagen = ImageDataGenerator(
    rotation_range = 30,
    brightness_range = [0.2,1.0],
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True,
    fill_mode = "nearest",
    rescale = 1./255,
    validation_split = val_size
)

validation_datagen = ImageDataGenerator(
    rotation_range = 30,
    brightness_range = [0.2,1.0],
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True,
    fill_mode = "nearest",
    rescale = 1./255,
    validation_split = val_size
)

# Train dan Validation
train_generator = train_datagen.flow_from_directory(
    dir_dataset,
    target_size = (150,150),
    color_mode = "rgb",
    class_mode = "categorical",
    batch_size = 16,
    shuffle = True,
    subset = "training"
)

validation_generator = validation_datagen.flow_from_directory(
    dir_dataset,
    target_size = (150,150),
    color_mode = "rgb",
    class_mode = "categorical",
    batch_size = 16,
    shuffle = False,
    subset = "validation"
)

#Model Sequential Using Conv2D dan MaxPooling
Model = Sequential(
    [
     Conv2D(32, (3,3), strides = (1,1), activation = 'relu' , input_shape = (150,150,3)),
     MaxPooling2D(pool_size = (2,2), padding = 'valid'),
     Conv2D(64, (3,3), strides = (1,1), activation = 'relu' ),
     MaxPooling2D(pool_size = (2,2), padding = 'valid'),
     Conv2D(128, (3,3), strides = (1,1), activation = 'relu' ),
     MaxPooling2D(pool_size = (2,2), padding = 'valid'),
     Flatten(),
     Dropout(0.2),
     Dense(128, activation = 'relu'),
     Dense(3, activation='softmax')
    ]
)

#Optimizer
Adam(learning_rate=0.00128, name='adam')
Model.compile(optimizer = 'adam',loss = 'categorical_crossentropy',metrics = ['accuracy'])

def scheduler(epoch, lr):
  if epoch < 5:
    return lr
  else:
    return lr * tf.math.exp(-0.1)

#Callback
lr_schedule = tf.keras.callbacks.LearningRateScheduler(scheduler, verbose=1)
tb_callback = tf.keras.callbacks.TensorBoard(
    log_dir='logs', histogram_freq=0, write_graph=True, write_images=False,
    update_freq='epoch', embeddings_freq=0,
    embeddings_metadata=None
)

Model.summary()

#Training
batch_size = 16
history = Model.fit(train_generator, 
                  epochs =  10, 
                  steps_per_epoch = 1333//batch_size,
                  validation_data = validation_generator, 
                  verbose = 1, 
                  validation_steps = 332//batch_size,
                  callbacks =[lr_schedule, tb_callback])

#Accuracy 
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
#Loss 
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

#Plot Accruracy
plt.plot(epochs, acc, 'r', label='Train Accuracy')
plt.plot(epochs, val_acc, 'g', label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend(loc=0)
plt.figure()
plt.show()

#Plot Loss
plt.plot(epochs, loss, 'r', label='Train Loss')
plt.plot(epochs, val_loss, 'g', label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend(loc=0)
plt.figure()
plt.show()

#Upload File
uploaded = files.upload()

#Condition
for file_upload in uploaded.keys():

  path = file_upload
  img = image.load_img(path, target_size=(150,150))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)

  images = np.vstack([x])
  classes = Model.predict(images, batch_size=16)

  if classes[0][0] == 1:
    print('Buah Mangga')
  elif classes[0][1] == 1:
    print('Buah Jeruk')
  else:
    print('Buah Pir')

#Ignore Warnings
warnings.filterwarnings('ignore')

#Convert Model to TF-Lite
converter = tf.lite.TFLiteConverter.from_keras_model(Model)
tflite_model = converter.convert()

#Save Model TF-Lite
with open('fruit_model.tflite', 'wb') as f:
  f.write(tflite_model)