#imports
import streamlit as st
import os 
import imageio


import tensorflow as tf
import numpy as np

from utils import load_video,num_to_char
from modelutil import load_model

# Set the layout as wide
st.set_page_config(layout='wide')


# Sidebar content
with st.sidebar:
    st.title('Trace Talk')
    st.image('lipreading.jpg')

# Generating a list of options and videos
options=os.listdir(os.path.join('..','data','s1'))
selected_video=st.selectbox('choose video',options)

#Generate 2 columns
col1,col2=st.columns(2)
if options:

    #Converting and Rendering the video

    with col1:
       st.info('The video below represents the chosen option from the dropdown menu')
       file_path=os.path.join('..','data','s1',selected_video)
       ffmpeg_path = r'C:\Path_Programs\ffmpeg.exe'
       os.system(f'{ffmpeg_path} -i {file_path} -vcodec libx264 test_video.mp4 -y')  #converting into a mp4 file format #libx264 is a library

        #Rendering inside of the app:
       video=open('test_video.mp4','rb')
       video_bytes=video.read()
       st.video(video_bytes)


    with col2: 
        st.info('This is all the machine learning model sees when making a prediction')
        video = load_video((file_path))

        imageio.mimwrite('cropped_video.mp4', video, fps=30)  # Save the cropped video
        st.video(open('cropped_video.mp4', 'rb').read())  # Display the cropped video

       

        st.info('This is the output of the machine learning model as tokens')
        model = load_model()
        yhat = model.predict(tf.expand_dims(video, axis=0))
        decoder = tf.keras.backend.ctc_decode(yhat, input_length=np.ones(yhat.shape[0])*yhat.shape[1], greedy=True)[0][0]
        decoder_array = decoder.numpy()
        decoder_array = decoder_array[0][decoder_array[0] != -1]

        st.text(decoder_array)

        # Convert prediction to text
        st.info('Final output after decoding the raw tokens into words')
        converted_prediction = tf.strings.reduce_join(num_to_char(decoder)).numpy().decode('utf-8')
        st.text(converted_prediction)

