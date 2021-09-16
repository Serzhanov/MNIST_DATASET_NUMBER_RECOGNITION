from PIL import Image
import numpy as np

def get_image(path):
    img = Image.open(path,'r')
    img=img.resize((28,28))
    img=img.convert('L')
    img=np.array(img)
    img=img.reshape(28,28)
    img=deleteting_zeros(img)
    return img

