import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from tensorflow import keras
from keras import layers
from traffic import *

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    data_dir = "C:/Users/sykri/PycharmProjects/CSCI_80/Week_5/traffic/gtsrb-small"

    # Get image arrays and labels for all image files
    images, labels = load_data(data_dir)

    print(len(labels))
    print(len(images))

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model1 = get_model()

    # Fit model on training data
    model1.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model1.evaluate(x_test,  y_test, verbose=2)

if __name__ == "__main__":
    main()