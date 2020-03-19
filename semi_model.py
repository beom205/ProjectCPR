import numpy as np
import keras
import cv2
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, MaxPooling2D
from keras.applications.resnet_v2 import ResNet50V2
from keras.layers import Conv2D

#from keras.applications.vgg16 import VGG16
import matplotlib.image as mpimg
from keras import backend as K
import matplotlib.pyplot as plt
%matplotlib inline

class SemiModel():
    def __init__(self, model_path):
        self.IMG_WIDTH = 220
        self.IMG_HEIGHT = 220
        self.model_path = model_path
        self.model = self.load_model()
        self.graph = tf.get_default_graph()

    def define_model(self):
        model = Sequential()
        model.add(ResNet50V2(weights=None, include_top = False, input_shape = (self.IMG_HEIGHT, self.IMG_WIDTH, 3)))
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

    def preprocessing_on_path(self, img_path):
        img = cv2.imread(img_path)
        img = cv2.resize(img, dsize=(self.IMG_WIDTH, self.IMG_HEIGHT))
        img = img / 255.0
        return img

    def predict_using_path(self, img_path):
        img = self.preprocessing_on_path(img_path)
        img = np.reshape(img, (1, self.IMG_HEIGHT, self.IMG_WIDTH, 3))
        with self.graph.as_default():
        	  predict_value = self.model.predict(img)
        	  prob = np.asscalar(predict_value)

        return prob

    def cam(self, img_path):
        
        #x = self.preprocessing_on_path(img_path)

        #model = VGG16(weights='imagenet')
        #model = self.load_model()

        model_layers = self.model.layers
        i = len(model_layers) - 1
        while(True):
            if i < 0:
                print('wrong model')
                break
            if type(self.model.layers[i]) == keras.layers.convolutional.Conv2D:
                last_conv_layer = model_layers[i]
                print('get conv')
                break
            i -= 1
        x = cv2.imread(img_path, 1)
        x = x/255.0
        x = cv2.resize(x, dsize=(220, 220))
        x = np.reshape(x, (1, 220, 220, 3))

        #last_conv_layer = self.model.get_layer('conv2d_6')

        grads = K.gradients(self.model.output, last_conv_layer.output)

        pooled_grads = K.mean(grads[0], axis=(0,1,2))

        iterate = K.function([self.model.input], [pooled_grads, last_conv_layer.output[0]])

        pooled_grads_value, conv_layer_output_value = iterate([x])

        for i in range(1024):
            conv_layer_output_value[:,:,i] *= pooled_grads_value[i]
        
        heatmap = np.mean(conv_layer_output_value, axis = -1)
        heatmap = np.maximum(heatmap,0)
        heatmap /= np.max(heatmap)

        x = cv2.imread(img_path, 1)
        heatmap = cv2.resize(heatmap, (x.shape[1], x.shape[0]))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        hif = .8
        superimposed_img = heatmap * hif + x
        output = 'gdrive/My Drive/output.jpeg'
        cv2.imwrite(output, superimposed_img)

        return output