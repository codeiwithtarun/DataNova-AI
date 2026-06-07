import pandas as pd


def smart_suggestions(dataframe):

    suggestions = []

    # -----------------------------------------
    # Dataset Shape
    # -----------------------------------------

    rows, cols = dataframe.shape

    suggestions.append(f"Dataset contains {rows} rows and {cols} columns.")

    # -----------------------------------------
    # Missing Values
    # -----------------------------------------

    missing_values = dataframe.isnull().sum()

    total_missing = missing_values.sum()

    if total_missing > 0:

        suggestions.append(
            f"Dataset has {total_missing} missing values."
        )

        missing_columns = missing_values[missing_values > 0]

        for column, count in missing_columns.items():

            suggestions.append(
                f"Column '{column}' contains {count} missing values."
            )

    else:

        suggestions.append("No missing values found.")

    # -----------------------------------------
    # Duplicate Rows
    # -----------------------------------------

    duplicate_count = dataframe.duplicated().sum()

    if duplicate_count > 0:

        suggestions.append(
            f"Dataset contains {duplicate_count} duplicate rows."
        )

    else:

        suggestions.append("No duplicate rows found.")

    # -----------------------------------------
    # Numeric Columns
    # -----------------------------------------

    numeric_columns = dataframe.select_dtypes(
        include=["int64", "float64"]
    ).columns

    suggestions.append(
        f"Dataset contains {len(numeric_columns)} numeric columns."
    )

    # -----------------------------------------
    # Categorical Columns
    # -----------------------------------------

    categorical_columns = dataframe.select_dtypes(
        include=["object"]
    ).columns

    suggestions.append(
        f"Dataset contains {len(categorical_columns)} categorical columns."
    )

    # -----------------------------------------
    # High Missing Warning
    # -----------------------------------------

    for column in dataframe.columns:

        missing_percent = (
            dataframe[column].isnull().sum() / len(dataframe)
        ) * 100

        if missing_percent > 40:

            suggestions.append(
                f"Column '{column}' has more than 40% missing values."
            )

    # -----------------------------------------
    # ML Readiness Score
    # -----------------------------------------

    score = 100

    score -= total_missing * 0.02

    score -= duplicate_count * 0.5

    if score < 0:
        score = 0

    suggestions.append(
        f"Estimated ML Readiness Score: {round(score, 2)} / 100"
    )

    # -----------------------------------------
    # Final Suggestion
    # -----------------------------------------

    if score > 80:

        suggestions.append(
            "Dataset looks good for Machine Learning."
        )

    elif score > 50:

        suggestions.append(
            "Dataset requires moderate cleaning before ML."
        )

    else:

        suggestions.append(
            "Dataset requires heavy cleaning before ML."
        )

    return suggestions