from PIL import Image
import numpy as np
import network
def recreating_arr_from_int_to_float(l):
    list_to_one_arr=[]
    for i in range(28):
        for j in range(28):
            l[0][j]=0
            if l[i][j]/255==1:
                l[i][j]=0
            x= float(l[i][j])/255.0
            list_to_one_arr.append(x)
    return list_to_one_arr

def get_image(path):
    img = Image.open(path, 'r')
    img = img.resize((28, 28))
    img = img.convert('L')
    img = np.array(img)
    network.visualize_input(img)
    img = recreating_arr_from_int_to_float(img)
    return img

