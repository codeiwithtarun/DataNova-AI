import streamlit as st


def upload_dataset():
    """
    Upload CSV or Excel dataset.
    """

    uploaded_file = st.file_uploader(
        label="Upload CSV or Excel File",
        type=["csv", "xlsx"]
    )

    return uploaded_file