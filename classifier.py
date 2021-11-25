from PIL import Image
import numpy as np
def deleteting_zeros(l):
    for i in range(28):
        #i always getting weird picture after transformation it to bits with 0 in every first line and column
        l[0][i] = 0
        l[i][0] = 0
        for j in range(28):
            if l[i][j]//255==1:
                l[i][j]=0
    return l

def recreating_arr_from_int_to_float(l):
    list_to_one_arr=[]
    for i in range(28):
        for j in range(28):
            x= float(l[i][j])/255.0
            list_to_one_arr.append(x)
    return list_to_one_arr

def get_image(path):
    img = Image.open(path,'r')
    img=img.resize((28,28))
    img=img.convert('L')
    img=np.array(img)
    img=deleteting_zeros(img)
    img=recreating_arr_from_int_to_float(img)
    return img

