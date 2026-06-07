def remove_duplicates(dataframe):

    cleaned_dataframe = dataframe.drop_duplicates()

    return cleaned_dataframe


def count_duplicates(dataframe):

    duplicate_count = dataframe.duplicated().sum()

    return duplicate_count