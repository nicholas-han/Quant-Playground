# import matplotlib.pyplot as plt
import tensorflow as tf
import logging


mnist = tf.keras.datasets.fashion_mnist
(trainImages, trainLabels), (testImages, testLabels) = mnist.load_data()

print(trainImages[0])