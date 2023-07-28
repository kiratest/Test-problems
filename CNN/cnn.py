import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten
from tensorflow.keras.callbacks import EarlyStopping

from sklearn.metrics import classification_report,confusion_matrix
import seaborn as sns


(x_train, y_train), (x_test, y_test) = mnist.load_data()


# Preprocessing Data
# We first need to make sure that the labels should be understandable by our CNN.
# Our labels are categories of numbers.
y_cat_test = to_categorical(y_test, 10)
y_cat_train = to_categorical(y_train, 10)


# Processing X Data
# We should normalize the X Data for the values to be between (0-1)
x_train = x_train / 255
x_test = x_test / 255


# Reshaping the data
# Our data is 60 000 images stored in 28 by 28 pixel array formation.
# Because we are dealing with 1 RGB channel (the images are black and white), we should add one
# more dimension. A color image would have 3 dimensions. 
x_train = x_train.reshape(60000, 28, 28, 1) # One channel
x_test = x_test.reshape(10000, 28, 28, 1)


# Training the Model
model = Sequential()

# Convolutional layer
model.add(Conv2D(filters=32, kernel_size=(4,4), input_shape=(28,28,1), activation='relu',))
# Pooling layer
model.add(MaxPool2D(pool_size=(2,2)))

# Flatten images from 28 by 28 to 764 before the final layer
model.add(Flatten())

# 128 neurons in dense hidden layer (number of neurons can be changed)
model.add(Dense(128, activation='relu'))

# Last layer is the classifier, therefore 10 possible classes
model.add(Dense(10, activation='softmax'))

# https://keras.io/metrics/
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print(model.summary())



early_stop = EarlyStopping(monitor='val_loss', patience=2)

# Train the Model
model.fit(x_train,y_cat_train,epochs=10,validation_data=(x_test,y_cat_test),callbacks=[early_stop])

# Evaluating the Model
print(model.metrics_names)

losses = pd.DataFrame(model.history.history)
print(losses.head())


losses[['accuracy','val_accuracy']].plot()
losses[['loss','val_loss']].plot()

print(model.metrics_names)
print(model.evaluate(x_test,y_cat_test,verbose=0))


predictions = model.predict_classes(x_test)
print(classification_report(y_test,predictions))
print(confusion_matrix(y_test,predictions))


plt.figure(figsize=(10,6))
sns.heatmap(confusion_matrix(y_test,predictions),annot=True)


# Predicting a given image
my_number = x_test[0]
plt.imshow(my_number.reshape(28,28))
model.predict_classes(my_number.reshape(1,28,28,1))
