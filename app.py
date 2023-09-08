import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page


st.set_page_config(
    page_title='Power Consumption Prediction App',
    page_icon='⚡',
   
)
page = st.sidebar.selectbox("Predict", ("Predict",))

show_predict_page()

