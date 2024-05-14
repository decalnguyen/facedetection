import cv2
import time
from pynput.keyboard import Controller

keyboard = Controller()

# Get the screen resolution
screen_width, screen_height = 1920, 1080  # Update with your screen resolution

cap = cv2.VideoCapture(0)

# Set the camera resolution to match the screen resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

keyboard = Controller()

# Define the key regions for the virtual keyboard
key_width = 50
key_height = 50
key_spacing = 10  # Adjust as needed

key_regions = {}
row_offset = 100
col_offset = 100

full_screen = False
final_text = ""

while True:
    if full_screen:
        cv2.namedWindow('Image', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    else:
        cv2.namedWindow('Image')

    success, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Check for key presses based on face position
        for key, (x_k, y_k, w_k, h_k) in key_regions.items():
            if x_k < x < x_k + w_k and y_k < y < y_k + h_k:
                cv2.rectangle(img, (x_k, y_k), (x_k + w_k, y_k + h_k), (0, 255, 0), 2)
                cv2.putText(img, key, (x_k + 10, y_k + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # Simulate key press when face is detected within key region
                keyboard.press(key)
                final_text += key

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('f'):  # Toggle full screen mode when 'f' is pressed
        full_screen = not full_screen
    elif key == 27:  # Press 'Esc' to exit the program
        break

cv2.destroyAllWindows()
cap.release()