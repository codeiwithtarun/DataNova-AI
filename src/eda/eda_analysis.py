import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def show_eda_analysis(dataframe):

    st.header("📊 Advanced EDA Analysis")

    # =========================================
    # DATASET PREVIEW
    # =========================================

    st.subheader("📄 Dataset Preview")

    preview_rows = st.slider(
        "Select Number of Rows",
        5,
        100,
        5
    )

    st.dataframe(
        dataframe.head(preview_rows)
    )

    # =========================================
    # BASIC INFORMATION
    # =========================================

    st.subheader("📌 Basic Dataset Information")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Rows",
        dataframe.shape[0]
    )

    col2.metric(
        "Columns",
        dataframe.shape[1]
    )

    col3.metric(
        "Missing Values",
        dataframe.isnull().sum().sum()
    )

    col4.metric(
        "Duplicate Rows",
        dataframe.duplicated().sum()
    )

    # =========================================
    # MEMORY USAGE
    # =========================================

    st.subheader("💾 Memory Usage")

    memory_usage = (
        dataframe.memory_usage(deep=True).sum()
        / 1024
    )

    st.write(
        f"Dataset Memory Usage: {memory_usage:.2f} KB"
    )

    # =========================================
    # DATA TYPES
    # =========================================

    st.subheader("🧬 Data Types")

    dtype_df = pd.DataFrame({
        "Column": dataframe.columns,
        "Data Type": dataframe.dtypes.astype(str)
    })

    st.dataframe(dtype_df)

    # =========================================
    # NULL VALUE ANALYSIS
    # =========================================

    st.subheader("🧩 Missing Value Analysis")

    missing_values = dataframe.isnull().sum()

    missing_df = pd.DataFrame({
        "Column": missing_values.index,
        "Missing Values": missing_values.values,
        "Missing Percentage": (
            missing_values.values
            / len(dataframe)
        ) * 100
    })

    st.dataframe(missing_df)

    # =========================================
    # MISSING VALUE CHART
    # =========================================

    st.subheader("📉 Missing Values Chart")

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    ax.bar(
        missing_df["Column"],
        missing_df["Missing Values"]
    )

    plt.xticks(rotation=90)

    st.pyplot(fig)

    # =========================================
    # UNIQUE VALUES
    # =========================================

    st.subheader("🔍 Unique Value Analysis")

    unique_df = pd.DataFrame({
        "Column": dataframe.columns,
        "Unique Values": [
            dataframe[col].nunique()
            for col in dataframe.columns
        ]
    })

    st.dataframe(unique_df)

    # =========================================
    # STATISTICAL SUMMARY
    # =========================================

    st.subheader("📈 Statistical Summary")

    st.dataframe(
        dataframe.describe()
    )

    # =========================================
    # NUMERIC & CATEGORICAL COLUMNS
    # =========================================

    numeric_cols = dataframe.select_dtypes(
        include=['number']
    ).columns

    categorical_cols = dataframe.select_dtypes(
        include=['object', 'string']
    ).columns

    st.subheader("📊 Column Type Summary")

    st.write(
        f"Numeric Columns: {len(numeric_cols)}"
    )

    st.write(
        f"Categorical Columns: {len(categorical_cols)}"
    )

    # =========================================
    # CORRELATION MATRIX
    # =========================================

    if len(numeric_cols) > 0:

        st.subheader("🔥 Correlation Heatmap")

        correlation = dataframe[
            numeric_cols
        ].corr()

        fig, ax = plt.subplots(
            figsize=(12, 8)
        )

        sns.heatmap(
            correlation,
            annot=True,
            cmap="coolwarm",
            ax=ax
        )

        st.pyplot(fig)

    # =========================================
    # DISTRIBUTION ANALYSIS
    # =========================================

    st.subheader("📉 Distribution Analysis")

    if len(numeric_cols) > 0:

        selected_num_col = st.selectbox(
            "Select Numeric Column",
            numeric_cols
        )

        fig, ax = plt.subplots()

        sns.histplot(
            dataframe[selected_num_col],
            kde=True,
            ax=ax
        )

        st.pyplot(fig)

    # =========================================
    # BOXPLOT ANALYSIS
    # =========================================

    st.subheader("📦 Boxplot Analysis")

    if len(numeric_cols) > 0:

        selected_box_col = st.selectbox(
            "Select Column for Boxplot",
            numeric_cols,
            key="boxplot"
        )

        fig, ax = plt.subplots()

        sns.boxplot(
            y=dataframe[selected_box_col],
            ax=ax
        )

        st.pyplot(fig)

    # =========================================
    # OUTLIER DETECTION
    # =========================================

    st.subheader("🚨 Outlier Detection")

    outlier_report = []

    for col in numeric_cols:

        Q1 = dataframe[col].quantile(0.25)

        Q3 = dataframe[col].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR

        upper = Q3 + 1.5 * IQR

        outliers = dataframe[
            (
                dataframe[col] < lower
            ) |
            (
                dataframe[col] > upper
            )
        ].shape[0]

        outlier_report.append(
            [col, outliers]
        )

    outlier_df = pd.DataFrame(
        outlier_report,
        columns=[
            "Column",
            "Outlier Count"
        ]
    )

    st.dataframe(outlier_df)

    # =========================================
    # SKEWNESS ANALYSIS
    # =========================================

    st.subheader("📐 Skewness Analysis")

    skewness_df = pd.DataFrame({
        "Column": numeric_cols,
        "Skewness": [
            dataframe[col].skew()
            for col in numeric_cols
        ]
    })

    st.dataframe(skewness_df)

    # =========================================
    # DUPLICATE ANALYSIS
    # =========================================

    st.subheader("♻ Duplicate Analysis")

    duplicate_rows = dataframe[
        dataframe.duplicated()
    ]

    st.write(
        f"Duplicate Rows Found: {duplicate_rows.shape[0]}"
    )

    if duplicate_rows.shape[0] > 0:

        st.dataframe(
            duplicate_rows.head()
        )

    # =========================================
    # COLUMN ANALYSIS
    # =========================================

    st.subheader("🧪 Advanced Column Analysis")

    selected_col = st.selectbox(
        "Select Column for Detailed Analysis",
        dataframe.columns,
        key="advanced_col"
    )

    st.write(
        "Data Type:",
        dataframe[selected_col].dtype
    )

    st.write(
        "Missing Values:",
        dataframe[selected_col].isnull().sum()
    )

    st.write(
        "Unique Values:",
        dataframe[selected_col].nunique()
    )

    # =========================================
    # NUMERIC COLUMN ANALYSIS
    # =========================================

    if selected_col in numeric_cols:

        st.write(
            "Mean:",
            dataframe[selected_col].mean()
        )

        st.write(
            "Median:",
            dataframe[selected_col].median()
        )

        st.write(
            "Mode:",
            dataframe[selected_col].mode()[0]
        )

        st.write(
            "Minimum:",
            dataframe[selected_col].min()
        )

        st.write(
            "Maximum:",
            dataframe[selected_col].max()
        )

        st.write(
            "Standard Deviation:",
            dataframe[selected_col].std()
        )

        st.write(
            "Variance:",
            dataframe[selected_col].var()
        )

    # =========================================
    # CATEGORICAL ANALYSIS
    # =========================================

    elif selected_col in categorical_cols:

        value_counts = dataframe[
            selected_col
        ].value_counts()

        st.dataframe(value_counts)

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        sns.countplot(
            x=dataframe[selected_col],
            ax=ax
        )

        plt.xticks(rotation=45)

        st.pyplot(fig)

    # =========================================
    # FEATURE CORRELATION
    # =========================================

    st.subheader("🔗 Strong Feature Correlations")

    if len(numeric_cols) > 1:

        corr_matrix = dataframe[
            numeric_cols
        ].corr()

        strong_corr = []

        for col1 in corr_matrix.columns:

            for col2 in corr_matrix.columns:

                if col1 != col2:

                    corr_value = corr_matrix.loc[
                        col1,
                        col2
                    ]

                    if abs(corr_value) > 0.7:

                        strong_corr.append(
                            [
                                col1,
                                col2,
                                corr_value
                            ]
                        )

        if len(strong_corr) > 0:

            strong_corr_df = pd.DataFrame(
                strong_corr,
                columns=[
                    "Feature 1",
                    "Feature 2",
                    "Correlation"
                ]
            )

            st.dataframe(
                strong_corr_df
            )

        else:

            st.info(
                "No Strong Correlations Found"
            )

    # =========================================
    # DATA QUALITY SCORE
    # =========================================

    st.subheader("🎯 Data Quality Score")

    quality_score = 100

    total_missing = dataframe.isnull().sum().sum()

    total_duplicates = dataframe.duplicated().sum()

    if total_missing > 0:

        quality_score -= 20

    if total_duplicates > 0:

        quality_score -= 10

    if quality_score < 0:

        quality_score = 0

    st.progress(
        quality_score / 100
    )

    st.success(
        f"Data Quality Score: {quality_score}/100"
    )

    # =========================================
    # AI INSIGHTS
    # =========================================

    st.subheader("🤖 AI Smart Insights")

    insights = []

    insights.append(
        f"Dataset contains {dataframe.shape[0]} rows and {dataframe.shape[1]} columns."
    )

    insights.append(
        f"Dataset has {len(numeric_cols)} numeric columns."
    )

    insights.append(
        f"Dataset has {len(categorical_cols)} categorical columns."
    )

    if total_missing > 0:

        insights.append(
            f"Dataset contains {total_missing} missing values."
        )

    else:

        insights.append(
            "No missing values found."
        )

    if total_duplicates > 0:

        insights.append(
            f"Dataset contains {total_duplicates} duplicate rows."
        )

    else:

        insights.append(
            "No duplicate rows found."
        )

    if quality_score >= 90:

        insights.append(
            "Dataset quality is excellent."
        )

    elif quality_score >= 70:

        insights.append(
            "Dataset quality is good."
        )

    else:

        insights.append(
            "Dataset requires more cleaning."
        )

    for insight in insights:

        st.success(insight)

    # =========================================
    # DOWNLOAD EDA REPORT
    # =========================================

    st.subheader("⬇ Download EDA Report")

    report_text = f"""
EDA REPORT

Rows: {dataframe.shape[0]}
Columns: {dataframe.shape[1]}
Missing Values: {total_missing}
Duplicate Rows: {total_duplicates}
Data Quality Score: {quality_score}/100
"""

    st.download_button(
        label="Download EDA Report",
        data=report_text,
        file_name="eda_report.txt",
        mime="text/plain"
    )
