import numpy as np
import keras
import cv2
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, MaxPooling2D
from keras.applications.resnet_v2 import ResNet50V2
from keras.layers import Conv2D
import tensorflow as tf

class SemiModel():
    def __init__(self, model_path):
        self.IMG_WIDTH = 220
        self.IMG_HEIGHT = 220
        self.model_path = model_path
        self.model = self.load_model()
        self.graph = tf.get_default_graph()

    def define_model(self):
        model = Sequential()
        model.add(ResNet50V2(weights = 'imagenet', include_top = False, input_shape = (self.IMG_HEIGHT, self.IMG_WIDTH, 3)))
        model.add(Conv2D(1024,kernel_size = (1,1), activation='relu', strides=(1, 1)))
        model.add(keras.layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001))
        model.add(Conv2D(1024,kernel_size = (3,3), activation='relu', strides=(1, 1)))
        model.add(MaxPooling2D(pool_size=(2, 2)))
		
        model.add(Conv2D(1024,kernel_size = (1,1), activation='relu', strides=(1, 1)))
        model.add(Flatten())
        model.add(Dense(512, activation='relu'))
        model.add(keras.layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001))
        model.add(Dense(1, activation='sigmoid'))
        return model

    def load_model(self):
        model = self.define_model()
        model.load_weights(self.model_path)
        return model

    def predict_using_path(self, img_path):
        img = self.preprocessing_on_path(img_path)
        img = np.reshape(img, (1, self.IMG_HEIGHT, self.IMG_WIDTH, 3))
        with self.graph.as_default():
        	predict_value = self.model.predict(img)
        	prob = np.asscalar(predict_value)

        return prob

    def preprocessing_on_path(self, img_path):
        img = cv2.imread(img_path)
        img = cv2.resize(img, dsize=(self.IMG_WIDTH, self.IMG_HEIGHT))
        img = img / 255.0
        return img