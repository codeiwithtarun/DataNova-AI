import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


def show_scatter_plot(dataframe):

    st.subheader("Scatter Plot")

    numeric_columns = dataframe.select_dtypes(
        include=['int64', 'float64']
    ).columns

    if len(numeric_columns) >= 2:

        x_column = st.selectbox(
            "Select X Axis",
            numeric_columns,
            key="scatter_x"
        )

        y_column = st.selectbox(
            "Select Y Axis",
            numeric_columns,
            key="scatter_y"
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        sns.scatterplot(
            x=dataframe[x_column],
            y=dataframe[y_column],
            ax=ax
        )

        st.pyplot(fig)

    else:
        st.warning("Need at least 2 numeric columns.")