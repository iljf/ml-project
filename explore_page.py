import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

def clean_age(x):
    if x > 50:
        return 50
    if x < 25:
        return 25
    return float(x)

def clean_workweekhrs(x):
    if x > 50:
        return 50
    if x < 35:
        return 35
    return float(x)



@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp", "Age", "WorkWeekHrs"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df['Age'] = df['Age'].apply(clean_age)
    df= df[df['Age'] != 49.5]
    df= df[df['Age'] != 26.8]
    df= df[df['Age'] != 32.5]
    df= df[df['Age'] != 31.5]
    df= df[df['Age'] != 39.5]
    df['WorkWeekHrs'] = df['WorkWeekHrs'].apply(clean_workweekhrs)
    df = df[df.groupby('WorkWeekHrs').WorkWeekHrs.transform('count')>10]
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
    st.title("해외 데이터 엔지니어 연봉 확인하기")

    st.write(
        """
    ### Stack Overflow Developer Survey
    """
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=False, startangle=270)
    ax1.axis("equal")

    st.write("""#### 나라별 데이터 표본 확인""")

    st.pyplot(fig1)
    
    st.write(
        """
    #### 나라별 평균 연봉
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### 경력별 평균 연봉
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)

    st.write(
        """
    #### 연령별 평균 연봉
    """
    )

    data = df.groupby(["Age"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)