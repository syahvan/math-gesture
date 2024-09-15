import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import google.generativeai as genai
from PIL import Image
import streamlit as st

# Configure the Streamlit page layout and title
st.set_page_config(layout="wide", page_title="Math with Gesture")
st.title("Math with Gesture 🔢🤌🏻")

# Create a toggle to run or stop the camera feed
run = st.toggle("Run Camera", value=True)
col1, col2 = st.columns([2,1])

# Column for displaying the webcam feed
with col1:
    FRAME_WINDOW = st.image([])

# Column for displaying instructions and AI-generated answers
with col2:
    st.subheader("How to Use 🤔")
    st.markdown('☝ **Raise your index finger** to draw.')
    st.markdown('👍 **Raise your thumb** to erase your drawing.')
    st.markdown('👌 **Raise your middle finger, ring finger, and pinky** to let the AI analyze the drawing.')

    st.subheader("Answer 💡")
    output_text_area = st.markdown("")

# Configure the Google Generative AI model
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize the webcam to capture video
cap = cv2.VideoCapture(1)
cap.set(3, 1280)  # Set frame width
cap.set(4, 720)   # Set frame height

# Initialize the HandDetector class with specific parameters
detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)

def getHandInfo(img):
    """
    Detects hands in the image and returns finger information and landmark list.
    """
    # Find hands in the current frame
    hands, img = detector.findHands(img, draw=False, flipType=True)
    
    # Check if any hands are detected
    if hands:
        hand = hands[0]  # Get the first hand detected
        lmList = hand["lmList"]  # List of 21 landmarks for the first hand

        # Count the number of fingers up for the first hand
        fingers = detector.fingersUp(hand)
        print(fingers)
        return fingers, lmList
    else:
        return None

def draw(info, prev_pos, canvas):
    """
    Draws on the canvas based on hand gestures and returns updated position and canvas.
    """
    fingers, lmList = info
    current_pos = None
    if fingers == [0, 1, 0, 0, 0]:
        # Draw when index finger is up
        current_pos = lmList[8][0:2]
        if prev_pos is None: prev_pos = current_pos
        cv2.line(canvas, current_pos, prev_pos, (0, 255, 0), 10)
    elif fingers == [1, 0, 0, 0, 0]:
        # Erase when thumb is up
        canvas = np.zeros_like(img)
    
    return current_pos, canvas

def sendToGemini(model, canvas, fingers):
    """
    Sends the canvas image to the AI model for analysis when specific fingers are raised.
    """
    if fingers == [0, 0, 1, 1, 1]:
        pil_image = Image.fromarray(canvas)
        response = model.generate_content(["Solve this math problem", pil_image])
        return response.text

prev_pos = None
canvas = None
image_combined = None
output_text = ""

# Continuously get frames from the webcam
while run:
    # Capture each frame from the webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip the image horizontally for a mirror effect
    
    if canvas is None:
        canvas = np.zeros_like(img)  # Initialize canvas if it does not exist

    info = getHandInfo(img)
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
        (0, 5), (5, 6), (6, 7), (7, 8),        # Index finger
        (0, 9), (9, 10), (10, 11), (11, 12),   # Middle finger
        (0, 13), (13, 14), (14, 15), (15, 16), # Ring finger
        (0, 17), (17, 18), (18, 19), (19, 20)  # Pinky
    ]
    
    if info:
        fingers, lmList = info
        # Draw hand connections and landmarks on the image
        for connection in connections:
            x1, y1, _ = lmList[connection[0]]
            x2, y2, _ = lmList[connection[1]]
            cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
        for lm in lmList:
            x, y, z = lm
            cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), cv2.FILLED)
        
        prev_pos, canvas = draw(info, prev_pos, canvas)
        output_text = sendToGemini(model, canvas, fingers)
    
    # Combine the drawn canvas with the webcam image and display it
    image_combined = cv2.addWeighted(img, 0.7, canvas, 0.3, 0)
    FRAME_WINDOW.image(image_combined, channels="BGR")
    
    # Display the AI-generated answer
    if output_text:
        output_text_area.text(output_text)
    
    # Keep the window open and update it for each frame; wait for 1 millisecond between frames
    cv2.waitKey(1)
