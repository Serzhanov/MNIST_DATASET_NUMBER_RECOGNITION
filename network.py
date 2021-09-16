
import numpy as np
from tensorflow import keras
from tensorflow.keras.layers import Dense
import tensorflow as tf
from tensorflow.keras.datasets import mnist

check=False
probability=0
def apprentisage():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    # standartization
    x_train = x_train / 255
    x_test = x_test / 255
    y_train_cat = keras.utils.to_categorical(y_train, 10)
    y_test_cat = keras.utils.to_categorical(y_test, 10)
    # model and layer creating
    global model
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28,28)),
        Dense(128, activation='relu'),
        Dense(50, activation='relu'),
        Dense(30, activation='relu'),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',  # optimizer
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(x_train, y_train_cat, batch_size=32, epochs=5, validation_split=0.2)
    val_loss, val_acc = model.evaluate(x_test, y_test_cat)  # evaluate the out of sample data with model
    return str(val_loss*100)+"%",str(val_acc*100)+"%"

def modeling(array):
    global check
    global probability
    if check==True:
        x = np.expand_dims(array, axis=0)
        res=model.predict(x)
        return np.argmax(res)
    else:
        check=True
        probability=apprentisage()
        return (modeling(array),probability)


