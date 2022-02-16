import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

page = st.sidebar.selectbox("경력예측 OR 대시보드", ("경력예측", "대시보드"))

if page == "경력예측":
    show_predict_page()
else:
    show_explore_page()