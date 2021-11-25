
import numpy as np
from tensorflow import keras
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
import tensorflow as tf
from tensorflow.keras.datasets import mnist
check=False
val_acc=0
val_loss=0
def apprentisage():
    global val_acc,val_loss
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train / 255.0
    x_test = x_test / 255.0
    x_train = x_train.reshape(x_train.shape[0], -1)
    x_test = x_test.reshape(x_test.shape[0], -1)
    print(x_train.shape)
    y_train_cat = keras.utils.to_categorical(y_train, 10)
    y_test_cat = keras.utils.to_categorical(y_test, 10)
    # model and layer creating
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units=128,input_shape=(784,),activation='relu'),
        Dense(128, activation='relu'),
        Dropout(0.25),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',  # optimizer
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(x_train, y_train_cat, batch_size=32, epochs=5)
    print(model.summary())
    val_loss, val_acc = model.evaluate(x_test, y_test_cat)  # evaluate the out of sample data with model
    print(val_loss,val_acc)
    return model

def modeling(array):
    checking_existing_of_model()
    global model
    x = np.expand_dims(array, axis=0)
    res=model.predict(x)
    return np.argmax(res)

def checking_existing_of_model():
    global check
    global model
    if check==False:
        model = apprentisage()
        check=True
