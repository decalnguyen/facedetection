# importing the cv2 library
import cv2
import numpy as np
from imgbeddings import imgbeddings
from PIL import Image
import psycopg2
from paho.mqtt import client as mqtt 


broker = 'broker.emqx.io'
port = 1883 
topic = "door/request"
def mqtt_connection():
    def connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
        else:
            print("Connection failed")
            
    client.on_connect = connect
    client.connect(broker, port)
    return client 
def publish(client, topic, msg):
    while True:
        time.sleep(1)
        error = client.publish(topic, msg)

        if error[0] == 0:
            print("Sent '{msg}' to topic '{topic}' ")
        else: 
            print("Failed to send message")
def Handdle_mqtt_function(msg):
    client = mqtt_connection()
    publish(client, topic, msg)





    
# loading the Haar Cascade algorithm file into alg variable
alg = "haarcascade_frontalface_default.xml"

# passing the algorithm to OpenCV
haar_cascade = cv2.CascadeClassifier(alg)

# loading the image path into file_name variable
file_name = 'image1.jpg'

# reading the image
img = cv2.imread(file_name, 0)

# creating a black and white version of the image
gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

# detecting the faces
faces = haar_cascade.detectMultiScale(gray_img, scaleFactor=1.05, minNeighbors=2, minSize=(100, 100))

# for each face detected
for x, y, w, h in faces:
    # crop the image to select only the face
    cropped_image = img[y : y + h, x : x + w]
    
    # loading the target image path into target_file_name variable
    target_file_name = 'image_detect.jpg'
    cv2.imwrite(target_file_name, cropped_image)

# loading the face image path into file_name variable
file_name = 'image_detect.jpg'

# opening the image
img = Image.open(file_name)

# loading the `imgbeddings`
ibed = imgbeddings()

# calculating the embeddings
embedding = ibed.to_embeddings(img)[0]

conn = psycopg2.connect("postgresql://postgres:test123@localhost:5432/cv_module")
cur = conn.cursor()
#cur.execute('INSERT INTO pictures values (%s,%s)', (file_name, embedding.tolist()))
conn.commit()
conn.close()

# loading the image path into file_name variable
file_name = 'tranthanh.jpg'

# reading the image
img = cv2.imread(file_name, 0)

# creating a black and white version of the image
gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

# detecting the faces
faces = haar_cascade.detectMultiScale(gray_img, scaleFactor=1.05, minNeighbors=2, minSize=(100, 100))

# for each face detected in the image
for x, y, w, h in faces:
    # crop the image to select only the face
    cropped_image = img[y : y + h, x : x + w]
    
    # Convert the NumPy array to a PIL image
    pil_image = Image.fromarray(cropped_image)
    
    ibed = imgbeddings()
    
    # calculating the embeddings
    slack_img_embedding = ibed.to_embeddings(pil_image)[0]

conn = psycopg2.connect("postgresql://postgres:test123@localhost:5432/cv_module")
cur = conn.cursor()
string_rep = "[" + ",".join(str(x) for x in slack_img_embedding.tolist()) + "]"
cur.execute("SELECT picture FROM pictures ORDER BY embedding <-> %s LIMIT 5;", (string_rep,))
rows = cur.fetchall()


if len(rows) > 0 :
    msg = bytes("OPEN", 'utf-8')
    Handdle_mqtt_function(msg)
else: 
    print("Khong co")