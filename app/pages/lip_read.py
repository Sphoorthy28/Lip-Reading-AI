import streamlit as st
import tensorflow as tf
import math
import dlib
import cv2
import numpy as np
from collections import deque

from keras import regularizers
from tensorflow.keras.layers import Conv3D, MaxPooling3D, Dense, Dropout, Flatten
from tensorflow.keras.models import Sequential
from keras.models import Sequential

TOTAL_FRAMES = 22
VALID_WORD_THRESHOLD = 2
NOT_TALKING_THRESHOLD = 10
PAST_BUFFER_SIZE = 4
LIP_WIDTH = 112
LIP_HEIGHT = 80


st.set_page_config(layout='wide', page_title="TRACE-TALK", page_icon="👄")
st.sidebar.success("Select a page above")

st.title("Can You Read My Lips?")

# label_dict = {6: 'hello', 5: 'dog', 10: 'my', 12: 'you', 9: 'lips', 3: 'cat', 11: 'read', 0: 'a', 4: 'demo', 7: 'here', 8: 'is', 1: 'bye', 2: 'can'}
label_dict = { 0:'lips', 3: 'demo', 1: 'zoom', 2: 'open', 4: 'webex'}
# label_dict = { 0:'open', 1: 'email'}


count = 0

# Define the input shape
# input_shape = (TOTAL_FRAMES, 80, 112, 3)
# Load the detector
detector = dlib.get_frontal_face_detector()

# Load the predictor
predictor = dlib.shape_predictor("/Users/sphoorthy/Desktop/Computer-Vision-Lip-Reading-2.0-main/data_collection/model/shape_predictor_68_face_landmarks.dat")

input_shape = (22, 80, 112, 3)

model = Sequential()
model.add(Conv3D(8, (3, 3, 3), activation='relu', input_shape=input_shape, kernel_regularizer=regularizers.l2(0.001)))
model.add(MaxPooling3D((2, 2, 2)))
model.add(Conv3D(32, (3, 3, 3), activation='relu', kernel_regularizer=regularizers.l2(0.001)))
model.add(MaxPooling3D((2, 2, 2)))
model.add(Conv3D(256, (3, 3, 3), activation='relu', kernel_regularizer=regularizers.l2(0.001)))
model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(label_dict), activation='softmax'))

model.load_weights('/Users/sphoorthy/Desktop/Computer-Vision-Lip-Reading-2.0-main/training/model_weights5.h5')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)

curr_word_frames = []
not_talking_counter = 0

first_word = True
labels = []

past_word_frames = deque(maxlen=PAST_BUFFER_SIZE)

ending_buffer_size = 5

predicted_word_label = None
draw_prediction = False

# spoken_already = []

# Function to resize the frame to fit Streamlit's column width
def resize_frame(frame, width):
    ratio = width / frame.shape[1]
    height = int(frame.shape[0] * ratio)
    return cv2.resize(frame, (width, height))

st.sidebar.title('Trace Talk')
st.sidebar.image('/Users/sphoorthy/Desktop/Computer-Vision-Lip-Reading-2.0-main/app/Images/lipreading.jpg')

# Placeholder for video frames
video_placeholder = st.empty()

# Create a "Start Talking" button
start_button = st.button('Start Talking')

# Create a "Stop Recording" button
stop_button = st.button('Stop Recording')

choice=''

if start_button:
    # Execute while loop when button is clicked
    while True:
        _, frame = cap.read()
        frame = resize_frame(frame, 640)  # Resize frame to fit Streamlit column width

        # Convert image into grayscale
        gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)

        # Use detector to find landmarks
        faces = detector(gray)

        for face in faces:
            x1 = face.left()    # left point
            y1 = face.top()     # top point
            x2 = face.right()   # right point
            y2 = face.bottom()  # bottom point

            # Create landmark object
            landmarks = predictor(image=gray, box=face)

            # Calculate the distance between the upper and lower lip landmarks
            mouth_top = (landmarks.part(51).x, landmarks.part(51).y)
            mouth_bottom = (landmarks.part(57).x, landmarks.part(57).y)
            lip_distance = math.hypot(mouth_bottom[0] - mouth_top[0], mouth_bottom[1] - mouth_top[1])

            lip_left = landmarks.part(48).x
            lip_right = landmarks.part(54).x
            lip_top = landmarks.part(50).y
            lip_bottom = landmarks.part(58).y

            # Add padding if necessary to get a 76x110 frame
            width_diff = LIP_WIDTH - (lip_right - lip_left)
            height_diff = LIP_HEIGHT - (lip_bottom - lip_top)
            pad_left = width_diff // 2
            pad_right = width_diff - pad_left
            pad_top = height_diff // 2
            pad_bottom = height_diff - pad_top

            # Ensure that the padding doesn't extend beyond the original frame
            pad_left = min(pad_left, lip_left)
            pad_right = min(pad_right, frame.shape[1] - lip_right)
            pad_top = min(pad_top, lip_top)
            pad_bottom = min(pad_bottom, frame.shape[0] - lip_bottom)

            # Create padded lip region
            lip_frame = frame[lip_top - pad_top:lip_bottom + pad_bottom, lip_left - pad_left:lip_right + pad_right]
            lip_frame = cv2.resize(lip_frame, (LIP_WIDTH, LIP_HEIGHT))

            lip_frame_lab = cv2.cvtColor(lip_frame, cv2.COLOR_BGR2LAB)
            # Apply contrast stretching to the L channel of the LAB image
            l_channel, a_channel, b_channel = cv2.split(lip_frame_lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(3,3))
            l_channel_eq = clahe.apply(l_channel)

            # Merge the equalized L channel with the original A and B channels
            lip_frame_eq = cv2.merge((l_channel_eq, a_channel, b_channel))
            lip_frame_eq = cv2.cvtColor(lip_frame_eq, cv2.COLOR_LAB2BGR)
            lip_frame_eq= cv2.GaussianBlur(lip_frame_eq, (7, 7), 0)
            lip_frame_eq = cv2.bilateralFilter(lip_frame_eq, 5, 75, 75)

            kernel = np.array([[-1,-1,-1],
                        [-1, 9,-1],
                        [-1,-1,-1]])

            # Apply the kernel to the input image
            lip_frame_eq = cv2.filter2D(lip_frame_eq, -1, kernel)
            lip_frame_eq= cv2.GaussianBlur(lip_frame_eq, (5, 5), 0)
            lip_frame = lip_frame_eq

            # Draw a circle around the mouth
            for n in range(48, 61):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(img=frame, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)

            if lip_distance > 40: # person is talking
                cv2.putText(frame, "Talking", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                curr_word_frames += [lip_frame.tolist()]

                not_talking_counter = 0
                draw_prediction = False
            else:
                cv2.putText(frame, "Not talking", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                not_talking_counter += 1
                if not_talking_counter >= NOT_TALKING_THRESHOLD and len(curr_word_frames) + PAST_BUFFER_SIZE == TOTAL_FRAMES:

                    curr_word_frames = list(past_word_frames) + curr_word_frames

                    curr_data = np.array([curr_word_frames[:input_shape[0]]])

                    print("***", curr_data.shape)
                    # print(spoken_already)
                    prediction = model.predict(curr_data)

                    prob_per_class = []
                    for i in range(len(prediction[0])):
                        prob_per_class.append((prediction[0][i], label_dict[i]))
                    sorted_probs = sorted(prob_per_class, key=lambda x: x[0], reverse=True)
                    for prob, label in sorted_probs:
                        print(f"{label}: {prob:.3f}")

                    predicted_class_index = np.argmax(prediction)
                    # while label_dict[predicted_class_index] in spoken_already:
                    #     # If the predicted label has already been spoken,
                    #     # set its probability to zero and choose the next highest probability
                    #     prediction[0][predicted_class_index] = 0
                    #     predicted_class_index = np.argmax(prediction)
                    predicted_word_label = label_dict[predicted_class_index]
                    # spoken_already.append(predicted_word_label)

                    print("FINISHED!", predicted_word_label)
                    choice+=predicted_word_label

                    draw_prediction = True
                    count = 0

                    curr_word_frames = []
                    not_talking_counter = 0
                elif not_talking_counter < NOT_TALKING_THRESHOLD and len(curr_word_frames) + PAST_BUFFER_SIZE < TOTAL_FRAMES and len(curr_word_frames) > VALID_WORD_THRESHOLD:
                    curr_word_frames += [lip_frame.tolist()]
                    not_talking_counter = 0
                elif len(curr_word_frames) < VALID_WORD_THRESHOLD or (not_talking_counter >= NOT_TALKING_THRESHOLD and len(curr_word_frames) + PAST_BUFFER_SIZE > TOTAL_FRAMES):
                    curr_word_frames = []

                past_word_frames+= [lip_frame.tolist()]
                if len(past_word_frames) > PAST_BUFFER_SIZE:
                    if past_word_frames:
                      past_word_frames.pop(0)

        if(draw_prediction and count < 20):
            count += 1
            cv2.putText(frame, predicted_word_label, (50 ,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)

        # Convert frame to bytes
        _, frame_bytes = cv2.imencode('.JPEG', frame)

        # Display frame in Streamlit
        video_placeholder.image(frame_bytes.tostring(), channels="BGR")

        key = cv2.waitKey(1)
        # if key == ord('q'):
        #     spoken_already = []

        # Check if the "Stop Recording" button is clicked
        if stop_button:
            st.write(choice)
            break

        # Exit when escape is pressed
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


