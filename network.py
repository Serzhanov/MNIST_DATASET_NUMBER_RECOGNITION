import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np
from tensorflow import keras
from tensorflow.keras.layers import Dense
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from keras.callbacks import History
check=False
val_acc=0
val_loss=0
res=0
(x_train, y_train), (x_test, y_test) = mnist.load_data()
hist=History()
def apprentisage():
    global val_acc,val_loss,hist,x_train,x_test
    x_train = x_train / 255.0
    x_test = x_test / 255.0
    x_train = x_train.reshape(x_train.shape[0], -1)
    x_test = x_test.reshape(x_test.shape[0], -1)
    y_train_cat = keras.utils.to_categorical(y_train, 10)
    y_test_cat = keras.utils.to_categorical(y_test, 10)
    # model and layer creating
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units=128,input_shape=(784,),activation='relu'),
        Dense(128, activation='relu'),
        Dense(10, activation='softmax')
    ])
    callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)
    model.compile(optimizer='adam',  # optimizer
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    hist=model.fit(x_train, y_train_cat, batch_size=32, epochs=50,validation_data=(x_train,y_train_cat),callbacks=[callback])
    plt.plot(hist.history['loss'])
    val_loss, val_acc = model.evaluate(x_test, y_test_cat)  # evaluate the out of sample data with model
    return model


def modeling(array):
    checking_existing_of_model()
    global model,res
    x = np.expand_dims(array, axis=0)
    res=model.predict(x)
    return (np.argmax(res),res[0][np.argmax(res)])

def checking_existing_of_model():
    global check
    global model
    if check==False:
        model = apprentisage()
        check=True

def analysis():
    global model,hist,x_test,y_test
    #Plot loss and val_loss

    plt.plot(hist.history['loss'],label="loss")
    plt.plot(hist.history['val_loss'],label="val_loss")
    plt.plot(hist.history['accuracy'],label="accuracy")
    plt.plot(hist.history['val_accuracy'],label="val_accuracy")
    plt.xlabel("Epochs")
    plt.ylabel("Validation  in %")
    plt.title("Graphic of fit")


    y_test = keras.utils.to_categorical(y_test, 10)#categorization for our matrix of confusin
    x_test = x_test.reshape(x_test.shape[0], -1)#reshape to matrice with 784 elemetns because in the begining Mnist gives us 28x28
    y_predicted=model.predict(x_test)
    y_predicted_classes = np.argmax(y_predicted, axis=1)
    y_true=np.argmax(y_test,axis=1)
    matrix=confusion_matrix(y_true,y_predicted_classes)
    #Plot
    plt.figure(1)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax = sns.heatmap(matrix, annot=True, fmt='d', ax=ax, cmap="Blues")
    ax.set_xlabel('Predicted Label')
    ax.set_ylabel('True Label')
    ax.set_title('Confusion Matrix')
    plt.title("Confusion Matrix")

    #Errors
    errors=(y_predicted_classes-y_true !=0)
    y_pred_classes_errors = y_predicted_classes[errors]
    y_pred_errors = y_predicted[errors]
    y_true_errors = y_true[errors]
    x_test_errors = x_test[errors]
    y_pred_errors_probability = np.max(y_pred_errors, axis=1)
    true_probability_errors = np.diagonal(np.take(y_pred_errors, y_true_errors, axis=1))
    diff_errors_pred_true = y_pred_errors_probability - true_probability_errors

    # Get list of indices of sorted differences
    sorted_idx_diff_errors = np.argsort(diff_errors_pred_true)
    top_idx_diff_errors = sorted_idx_diff_errors[-5:]  # 5 last ones

    # Show Top Errors
    num = len(top_idx_diff_errors)
    plt.figure(2)

    f, ax = plt.subplots(1, num, figsize=(30, 30))
    f.suptitle("Last 5 errors on the validation data")

    for i in range(0, num):
        idx = top_idx_diff_errors[i]
        sample = x_test_errors[idx].reshape(28, 28)
        y_t = y_true_errors[idx]
        y_p = y_pred_classes_errors[idx]
        ax[i].imshow(sample, cmap='gray')
        ax[i].set_title("Predicted label :{}\nTrue label: {}".format(y_p, y_t), fontsize=12)

    plt.show()

def visualize_input(img):
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111)
    ax.imshow(img, cmap='gray')
    width, height = (28,28)
    thresh = img.max()/2.5
    for x in range(width):
        for y in range(height):
            ax.annotate(str(round(img[x][y],2)), xy=(y,x),
                        horizontalalignment='center',
                        verticalalignment='center',
                        color='white' if img[x][y]<thresh else 'black')

