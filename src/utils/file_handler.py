import pandas as pd
import streamlit as st


def load_dataset(uploaded_file):
    """
    Load CSV or Excel dataset safely.
    """

    try:

        # CSV FILE
        if uploaded_file.name.endswith(".csv"):

            dataframe = pd.read_csv(uploaded_file)

        # EXCEL FILE
        elif uploaded_file.name.endswith(".xlsx"):

            dataframe = pd.read_excel(uploaded_file)

        else:

            st.error("Unsupported file format.")
            return None

        return dataframe

    except Exception as error:

        st.error(f"Error loading dataset: {error}")

        return None