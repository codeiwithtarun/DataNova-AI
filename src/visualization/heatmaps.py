import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


def show_heatmap(dataframe):

    st.subheader("Correlation Heatmap")

    numeric_dataframe = dataframe.select_dtypes(
        include=['int64', 'float64']
    )

    if len(numeric_dataframe.columns) > 1:

        correlation = numeric_dataframe.corr()

        fig, ax = plt.subplots(figsize=(10, 6))

        sns.heatmap(
            correlation,
            annot=True,
            cmap="coolwarm",
            ax=ax
        )

        st.pyplot(fig)

    else:
        st.warning("Not enough numeric columns found.")