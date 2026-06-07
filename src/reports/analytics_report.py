import streamlit as st
import pandas as pd


def generate_report(dataframe):

    st.subheader("Dataset Analytics Report")

    # ------------------------------------------------
    # DATASET SHAPE
    # ------------------------------------------------

    rows, columns = dataframe.shape

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", rows)

    with col2:
        st.metric("Columns", columns)

    st.markdown("---")

    # ------------------------------------------------
    # MISSING VALUES
    # ------------------------------------------------

    st.subheader("Missing Values Summary")

    missing_values = dataframe.isnull().sum()

    missing_dataframe = pd.DataFrame({
        "Column": missing_values.index,
        "Missing Values": missing_values.values
    })

    st.dataframe(missing_dataframe)

    st.markdown("---")

    # ------------------------------------------------
    # DUPLICATE ROWS
    # ------------------------------------------------

    st.subheader("Duplicate Rows")

    duplicate_rows = dataframe.duplicated().sum()

    st.info(f"Duplicate Rows Found: {duplicate_rows}")

    st.markdown("---")

    # ------------------------------------------------
    # DATA TYPES
    # ------------------------------------------------

    st.subheader("Column Data Types")

    datatype_dataframe = pd.DataFrame({
        "Column": dataframe.dtypes.index,
        "Data Type": dataframe.dtypes.values})
    st.dataframe(datatype_dataframe)