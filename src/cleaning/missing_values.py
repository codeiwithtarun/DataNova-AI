import pandas as pd


def remove_missing_values(dataframe):

    cleaned_dataframe = dataframe.dropna()

    return cleaned_dataframe


def fill_missing_values(dataframe):

    dataframe = dataframe.copy()

    for column in dataframe.columns:

        if dataframe[column].dtype == "object":

            mode_value = dataframe[column].mode()[0]

            dataframe[column] = dataframe[column].fillna(mode_value)

        else:

            mean_value = dataframe[column].mean()

            dataframe[column] = dataframe[column].fillna(mean_value)

    return dataframe


def missing_values_summary(dataframe):

    missing_data = dataframe.isnull().sum()

    missing_data = missing_data[missing_data > 0]

    return missing_data