# importing the required libraries
import numpy as np
from imgbeddings import imgbeddings
from PIL import Image

# loading the face image path into file_name variable
file_name = '<INSERT YOUR FACE FILE NAME> (X2.jpg)'

# opening the image
img = Image.open(file_name)

# loading the `imgbeddings`
ibed = imgbeddings()

# calculating the embeddings
embedding = ibed.to_embeddings(img)[0]