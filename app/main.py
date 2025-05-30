import streamlit as st

st.title('Cold Email Generator')
url = st.text_input('Enter a URL:')

submit_button = st.button('Submit')

if submit_button:
    st.code('Hello', language='markdown')