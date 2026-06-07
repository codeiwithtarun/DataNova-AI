import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


def show_boxplot(dataframe):

    st.subheader("Box Plot")

    numeric_columns = dataframe.select_dtypes(
        include=['int64', 'float64']
    ).columns

    if len(numeric_columns) > 0:

        selected_column = st.selectbox(
            "Select Column",
            numeric_columns,
            key="boxplot_column"
        )

        fig, ax = plt.subplots(figsize=(8, 4))

        sns.boxplot(
            x=dataframe[selected_column],
            ax=ax
        )

        st.pyplot(fig)

    else:
        st.warning("No numeric columns found.")