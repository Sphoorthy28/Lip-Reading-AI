import streamlit as st

def main():
    st.set_page_config(layout='wide', page_title="About Us", page_icon="👄")
    st.sidebar.image("/Users/sphoorthy/Desktop/Computer-Vision-Lip-Reading-2.0-main/app/Images/lipreading.jpg", use_column_width=True)

    st.sidebar.success("Select a page above")

    st.title("About Us")

    st.write("""
     In a world where effective communication is key, lipreading plays a crucial role for individuals with hearing impairments.
    Trace Talk is a real-time lip reading application developed to assist individuals in understanding speech through lip movements.
    By leveraging advanced computer vision and machine learning techniques, Trace Talk accurately interprets lip movements in real-time,
    providing a valuable tool for those who rely on lipreading to communicate effectively in their daily lives.
    """)

    st.header("Key Features:")
    st.write("- Real-time lip reading")
    st.write("- Text interpretation")
    st.write("- User-friendly interface")

    st.title("Meet the team")
    # Display images and content side by side
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image('/Users/sphoorthy/Desktop/Computer-Vision-Lip-Reading-2.0-main/app/Images/adithi.jpeg', caption='Adithi', use_column_width=True)
        st.write("Frontend developer")

    with col2:
        st.image('/Users/sphoorthy/Desktop/Computer-Vision-Lip-Reading-2.0-main/app/Images/ashutosh.jpeg', caption='Ashutosh', use_column_width=True)
        st.write("Frontend developer")

    with col3:
        st.image('/Users/sphoorthy/Desktop/Computer-Vision-Lip-Reading-2.0-main/app/Images/nabeela.jpeg', caption='Nabeela', use_column_width=True)
        st.write("Full stack developer")

    with col4:

        st.image('/Users/sphoorthy/Desktop/Computer-Vision-Lip-Reading-2.0-main/app/Images/sphoorthy.jpeg', caption='Spoorthy', use_column_width=True)
        st.write("Full stack developer")

    with col5:
        st.image('/Users/sphoorthy/Desktop/Computer-Vision-Lip-Reading-2.0-main/app/Images/vaibhav.jpeg', caption='Vaibhav', use_column_width=True)
        st.write("Full stack developer")



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