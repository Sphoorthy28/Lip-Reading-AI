import streamlit as st

def main():

    # Set page config and sidebar
    st.set_page_config(layout='wide', page_title="TRACE-TALK", page_icon="👄")
    st.sidebar.success("Select a page above")
    # Adding image to the sidebar
    st.sidebar.image("/Users/sphoorthy/Desktop/Computer-Vision-Lip-Reading-2.0-main/app/Images/lipreading.jpg", use_column_width=True)

    # CSS for increasing font size of titles
    st.write(
    """
    <style>
        /* Increase font size for titles */
        .css-1l05mrh {
            font-size: 40px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
   )

# Title with increased font size
    st.title("Trace Talk")
    st.write("Real-Time Lip Reading Web Application")


    # Main content container
    main_container = st.container()

    with main_container:
        # Video, Empty Column, and Instructions section
        col1, col2, col3 = st.columns([1, 0.5, 3])

        with col1:
            # Instructions section
            st.header("Instructions:")
            st.write("1. Ensure you are in a well-lit environment.")
            st.write("2. Position your face in front of the camera.")
            st.write("3. Click on the 'Start Recording' button to initiate lip reading.")
            st.write("")

        with col3:
            # Local video file path
            video_path = "/Users/sphoorthy/Desktop/Computer-Vision-Lip-Reading-2.0-main/app/live.mp4"

            # Display video
            st.video(video_path)

      # Get Started section
        st.header("Get Started:")
        st.write("Click on the 'lip read' page from the sidebar to start lip reading.")
        # st.write("")
        st.write("Navigate to the 'New Word' page to add a new word to the lip reading dataset.")
        st.write("Learn more about Trace Talk and its development by visiting the 'About Us' page from the sidebar.")

    st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
       background-color: #1c1c1c; /* Darker shade of grey */
        padding: 10px 0;
        text-align: center;
        font-size: 12px;
        color: #fff;
        z-index: 1000; /* Ensure the footer stays on top of other elements */
    }
    </style>
    <div class="footer">
        Contact us at: lci2021019@iiitl.ac.in | +918985415780 | IIIT Lucknow, Ahmamau,Uttar Pradesh, India, 226002
        <br>
        ©2024 by TraceTalk
    </div>
    """,
    unsafe_allow_html=True
  )

if __name__ == "__main__":
    main()