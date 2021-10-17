import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

st.set_page_config(layout="wide")

def remove_outliers(df, category = None, input = None):
    if category is None or input is None:
        Q1 = df['math score'].quantile(0.25)
        Q3 = df['math score'].quantile(0.75)
    else:
        Q1 = df[df[category] == input[category]]['math score'].quantile(0.25)
        Q3 = df[df[category] == input[category]]['math score'].quantile(0.75)
    IQR = Q3 - Q1

    df = df[~((df['math score'] < (Q1 - 1.5 * IQR)) | (df['math score'] > (Q3 + 1.5 * IQR)))]
    return df

def main():
    df = pd.read_csv('exams.csv')
    Input = {}

    col1,col2  = st.columns([2,2])
    buttonPress = False
    with col1:
        st.title("Hello")

    with col2:
        Input["gender"] = st.radio('Gender', ['male', 'female'])
        Input["parental level of education"] = st.selectbox('Parental level of education', ["associate's degree", "some high school", "high school", "master's degree", "some college", "bachelor's degree"])


        Input["lunch"] = st.radio('Have you lunch ?', ['standard', 'free/reduced'])
        Input["test preparation course"] = st.radio("Are you preparing for the assessment ?", ["none", "completed"])

        buttonPress = st.button('Click me')
        if buttonPress:
            print(Input)

    if buttonPress:
        col3, col4, col5 = st.columns([2, 2, 2])
        with col3:
            st.write("Here you can see the median of math score for all people")
            dfAll = pickle.loads(pickle.dumps(df))
            dfAll = remove_outliers(dfAll)
            fig = px.box(dfAll, y="math score", width=450, height=450)
            st.plotly_chart(fig)
        with col4:
            st.write("Here you can see the median of math score for female people")
            dfGender = pickle.loads(pickle.dumps(df))
            dfGender = remove_outliers(dfGender, "gender", Input)
            fig = px.box(dfGender[dfGender["gender"] == Input["gender"]], y="math score",  width=450, height=450)
            st.plotly_chart(fig)
        with col5:
            st.write("Here you can see the median of math score with your parental level of education")
            dfLevelEducation = pickle.loads(pickle.dumps(df))
            dfLevelEducation = remove_outliers(dfLevelEducation, "parental level of education", Input)
            fig = px.box(dfLevelEducation[dfLevelEducation["parental level of education"] == Input["parental level of education"]], y="math score",  width=450, height=450)
            st.plotly_chart(fig)
        col6, col7, col8 = st.columns([2, 2, 2])
        with col6:
            st.write("Here you can see the median of math score with your lunch")
            dfLunch = pickle.loads(pickle.dumps(df))
            dfLunch = remove_outliers(dfLunch, "lunch", Input)
            fig = px.box(dfLunch[dfLunch["lunch"] == Input["lunch"]], y="math score",  width=450, height=450)
            st.plotly_chart(fig)
        with col7:
            st.write("Here you can see the median of math score with your test preparation course")
            dfTestPreparation = pickle.loads(pickle.dumps(df))
            dfTestPreparation = remove_outliers(dfTestPreparation, "test preparation course", Input)
            fig = px.box(dfTestPreparation[dfTestPreparation["test preparation course"] == Input["test preparation course"]], y="math score",  width=450, height=450)
            st.plotly_chart(fig)


if __name__ == '__main__':
	main()