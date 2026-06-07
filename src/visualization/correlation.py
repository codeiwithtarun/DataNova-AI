import streamlit as st


def show_correlation_matrix(dataframe):

    st.subheader("Correlation Matrix")

    numeric_dataframe = dataframe.select_dtypes(
        include=['int64', 'float64']
    )

    correlation = numeric_dataframe.corr()

    st.dataframe(correlation)