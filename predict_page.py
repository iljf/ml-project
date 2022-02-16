import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("나의 경력으로 해외에서는 연봉을 얼마나 받을 수 있을까?")

    st.write("""### 정보를 입력해주세요.""")

    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degre",
        "Master’s degree",
        "Post grad",
    )

    country = st.selectbox("나라를 선택하세요.", countries)
    education = st.selectbox("학력을 선택하세요.", education)
    experience = st.slider("경력을 선택하세요.", 0, 50, 3)
    age = st.slider("나이를 선택하세요.", 25, 50, 30)
    workhr = st.slider("주 근무시간을 선탁하세요.", 35, 50, 37)


    ok = st.button("연봉 계산하기")
    if ok:
        X = np.array([[country, education, experience, age, workhr]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X = X.astype(float)

        salary = regressor.predict(X)
        salary2 = ((salary)*1200) / 10000
        st.subheader(f"계산된 예산 연봉은 {salary2[0]:.0f}만원 입니다.")