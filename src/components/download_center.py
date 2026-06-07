import streamlit as st


def download_dataset(dataframe):

    csv_file = dataframe.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Cleaned Dataset",
        data=csv_file,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )