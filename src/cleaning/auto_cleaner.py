import pandas as pd


def auto_clean_dataset(dataframe):

    cleaned_dataframe = dataframe.copy()

    # -----------------------------------------
    # REMOVE DUPLICATES
    # -----------------------------------------

    cleaned_dataframe = cleaned_dataframe.drop_duplicates()

    # -----------------------------------------
    # HANDLE MISSING VALUES
    # -----------------------------------------

    for column in cleaned_dataframe.columns:

        # Numeric Columns
        if cleaned_dataframe[column].dtype in ["int64", "float64"]:

            cleaned_dataframe[column] = cleaned_dataframe[column].fillna(
                cleaned_dataframe[column].mean()
            )

        # Categorical Columns
        else:

            cleaned_dataframe[column] = cleaned_dataframe[column].fillna(
                cleaned_dataframe[column].mode()[0]
            )

    # -----------------------------------------
    # RESET INDEX
    # -----------------------------------------

    cleaned_dataframe = cleaned_dataframe.reset_index(drop=True)

    return cleaned_dataframe