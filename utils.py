import tensorflow as tf
from typing import List
import cv2
import os 
import imageio

#these lines of code set up mappings between characters and integers 
vocab = [x for x in "abcdefghijklmnopqrstuvwxyz'?!123456789 "]
char_to_num = tf.keras.layers.StringLookup(vocabulary=vocab, oov_token="")
# Mapping integers back to original characters
num_to_char = tf.keras.layers.StringLookup(vocabulary=char_to_num.get_vocabulary(), oov_token="", invert=True)

# This function loads and preprocesses frames from a video file, preparing them for input into model:
def load_video(path:str) -> List[float]: 
    #print(path)
    cap = cv2.VideoCapture(path) #This line initializes a video capture object
    frames = []
    for _ in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))): #which retrieves the total number of frames in the video.
        ret, frame = cap.read()   #This line reads the next frame from the video capture object. 
        frame = tf.image.rgb_to_grayscale(frame)   #This line converts the RGB frame to grayscale
        frames.append(frame[190:236,80:220,:])    #This line appends a cropped mouth region of the frame to the frames list
    cap.release()
    
    mean = tf.math.reduce_mean(frames)
    std = tf.math.reduce_std(tf.cast(frames, tf.float32))
    return tf.cast((frames - mean), tf.float32) / std  #The above 3 lines normalizes the pixel intensities of all frames in the video.


