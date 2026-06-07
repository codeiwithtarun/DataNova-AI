import streamlit as st
import pandas as pd


def show_dataset_preview(dataframe):
    """
    Display dataset preview and information.
    """

    st.subheader("Dataset Preview")

    st.dataframe(dataframe)

    st.markdown("---")

    # DATASET SHAPE
    st.subheader("Dataset Shape")

    rows, columns = dataframe.shape

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", rows)

    with col2:
        st.metric("Columns", columns)

    st.markdown("---")

    # COLUMN NAMES
    st.subheader("Column Names")

    st.write(list(dataframe.columns))

    st.markdown("---")

    # DATA TYPES
    st.subheader("Data Types")

    datatype_dataframe = pd.DataFrame(
        dataframe.dtypes,
        columns=["Data Type"]
    )

    st.dataframe(datatype_dataframe)

    st.markdown("---")

    # MISSING VALUES
    st.subheader("Missing Values")

    missing_values = dataframe.isnull().sum()

    missing_dataframe = pd.DataFrame({
        "Column": missing_values.index,
        "Missing Values": missing_values.values
    })

    st.dataframe(missing_dataframe)

    st.markdown("---")

    # MEMORY USAGE
    st.subheader("Memory Usage")

    memory_usage = dataframe.memory_usage(deep=True).sum()

    memory_usage_mb = memory_usage / (1024 * 1024)

    st.write(f"Memory Usage: {memory_usage_mb:.2f} MB")