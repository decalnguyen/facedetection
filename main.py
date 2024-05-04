# importing the cv2 library
import cv2

# loading the Haar Cascade algorithm file into alg variable
alg = "haarcascade_frontalface_default.xml"

# passing the algorithm to OpenCV
haar_cascade = cv2.CascadeClassifier(alg)

# loading the image path into file_name variable
file_name = '<INSERT YOUR IMAGE NAME HERE> for eg-> X1.jpg'

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
    target_file_name = '<INSERT YOUR OUTPUT FACE IMAGE NAME HERE> for eg-> X2.jpg'
    cv2.imwrite(target_file_name, cropped_image)